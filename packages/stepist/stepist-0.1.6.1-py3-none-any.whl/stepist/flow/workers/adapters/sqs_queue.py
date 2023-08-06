import boto3
import ujson
import time
import multiprocessing

from stepist.flow.workers.worker_engine import BaseWorkerEngine


class SQSAdapter(BaseWorkerEngine):
    def __init__(self, session=boto3, visibility_timeout=None,
                 message_retention_period=None, wait_seconds=5,
                 data_pickler=ujson):

        self.data_pickler = data_pickler

        self.session = session
        self.sqs_client = session.client('sqs')
        self.sqs_resource = session.resource('sqs')

        self.message_retention_period = message_retention_period
        self.visibility_timeout = visibility_timeout
        self.wait_seconds = wait_seconds

        self._queues = dict()
        self._steps = dict()

    def add_job(self, step, data, **kwargs):
        queue_name = self.get_queue_name(step)

        queue = self._queues.get(queue_name, None)
        if not queue:
            raise RuntimeError("Queue %s not found" % queue_name)

        kwargs = {
            'MessageBody': self.data_pickler.dumps(data.get_dict()),
            'MessageAttributes': {},
            'DelaySeconds': 0
        }

        queue.send_message(**kwargs)

    def add_jobs(self, step, jobs_data, **kwargs):
        for job_data in jobs_data:
            self.add_job(step, job_data, **kwargs)

    def receive_job(self, step, wait_seconds=5):
        q_name = self.get_queue_name(step)
        queue = self.session.resource('sqs').get_queue_by_name(
            QueueName=q_name)

        kwargs = {
            'WaitTimeSeconds': wait_seconds,
            'MaxNumberOfMessages': 1,
            'MessageAttributeNames': ['All'],
            'AttributeNames': ['All'],
        }
        messages = queue.receive_messages(**kwargs)
        if not messages:
            return None

        if len(messages) != 1:
            raise RuntimeError("Got more than 1 job for some reason")

        msg = messages[0]

        msg_result = {
            'Id': msg.message_id,
            'ReceiptHandle': msg.receipt_handle
        }
        queue.delete_messages(Entries=[msg_result])

        return self.data_pickler.loads(msg.body)

    def process(self, *steps, die_when_empty=False, die_on_error=True):
        queues = []
        for step in steps:
            queues.append(self.get_queue_name(step))

        if not queues:
            return

        mng = multiprocessing.Manager()
        empty_queues = mng.dict({q: False for q in queues})

        processes = []
        for queue_name in queues:
            p = multiprocessing.Process(
                target=self.process_queue,
                kwargs={
                    'queue_name': queue_name,
                    'die_on_error': die_on_error,
                    'empty_queues': empty_queues,
                    'die_when_empty': die_when_empty,
                },
            )
            p.start()
            processes.append(p)

        for p in processes:
            p.join()
            p.terminate()

    def process_queue(self, queue_name, die_on_error, empty_queues,
                      die_when_empty):
        try:
            queue = self.session.resource('sqs').get_queue_by_name(QueueName=queue_name)
        except Exception:
            empty_queues[queue_name] = True
            raise

        if not queue_name or not queue:
            empty_queues[queue_name] = True
            return

        while True:
            kwargs = {
                'WaitTimeSeconds': self.wait_seconds,
                'MaxNumberOfMessages': 10,
                'MessageAttributeNames': ['All'],
                'AttributeNames': ['All'],
            }
            messages = queue.receive_messages(**kwargs)

            if not messages:
                empty_queues[queue_name] = True
                if all(list(empty_queues.values())) and die_when_empty:
                    exit()

                time.sleep(self.wait_seconds)
                continue

            empty_queues[queue_name] = False

            msg_results = []
            for msg in messages:
                data = self.data_pickler.loads(msg.body)
                try:
                    self._steps[queue_name].receive_job(**data)
                except Exception:
                    empty_queues[queue_name] = True
                    if die_on_error:
                        raise

                msg_results.append({
                    'Id': msg.message_id,
                    'ReceiptHandle': msg.receipt_handle
                })

            if msg_results:
                queue.delete_messages(Entries=msg_results)

    def flush_queue(self, step):
        raise NotImplemented("Not implemented yet. Delete queue using "
                             "SQS dashboard")

    def jobs_count(self, *steps):
        jobs = 0

        for step in steps:
            queue_name = self.get_queue_name(step)
            sqs_q = self.sqs_client.get_queue_url(QueueName=queue_name)
            attrs = self.sqs_client.get_queue_attributes(
                sqs_q, ['ApproximateNumberOfMessages'])
            jobs += attrs.get("ApproximateNumberOfMessages", 0)

        return jobs

    def register_worker(self, step):
        queue_name = self.get_queue_name(step)

        attrs = {}
        kwargs = {
            'QueueName': queue_name,
            'Attributes': attrs,
        }
        if self.message_retention_period is not None:
            attrs['MessageRetentionPeriod'] = str(self.message_retention_period)
        if self.visibility_timeout is not None:
            attrs['VisibilityTimeout'] = str(self.visibility_timeout)

        self.sqs_client.create_queue(**kwargs)

        queue = self.sqs_resource.get_queue_by_name(QueueName=queue_name)

        self._queues[queue_name] = queue
        self._steps[queue_name] = step

    def monitor_steps(self, step_keys, monitoring_for_sec):
        pass

    def get_queue_name(self, step):
        return step.step_key().replace(":", "-")


def _move_first_to_the_end(a):
    return a[1:] + [a[0]]


class DieWhenEmpty:
    def __init__(self, active, queues):
        self.active = active
        self.queues = queues

        self.queus_no_jobs = set()

    def update_status(self, queue_name, no_job):
        if no_job:
            self.queus_no_jobs.add(queue_name)
        elif queue_name in self.queus_no_jobs:
            self.queus_no_jobs.remove(queue_name)

    def __bool__(self):
        return len(self.queus_no_jobs) >= len(self.queues)
