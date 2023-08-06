import ujson
from stepist.flow.steps import Step, FactoryStep

from stepist.app_config import AppConfig
from stepist.dbs import DBs
from stepist.flow import workers

from stepist.flow.workers import simple_multiprocessing
from stepist.flow.workers.adapters import simple_queue
from stepist.flow.workers import reducer_engine

from stepist.flow.steps.reducer_step import ReducerStep

from stepist.flow.workers.boost import sockets


class App:

    def __init__(self, worker_engine=None, use_booster=False, booster=None,
                 data_pickler=ujson, **config_kwargs):
        self.steps = dict()
        self.default_dbs = None
        self.verbose = None
        self.use_booster = use_booster

        self.data_pickler = data_pickler

        self.config = AppConfig(**{**AppConfig.init_default(),
                                   **config_kwargs})
        self.load_config(self.config)

        self.worker_engine = worker_engine
        self.booster = booster

        if self.worker_engine is None:
            self.worker_engine = simple_queue.SimpleQueueAdapter(
                self.default_dbs.redis_db,
                data_pickler=self.data_pickler
            )

        self.reducer_engine = reducer_engine.RedisReducerEngine(
            app=self,
            redis_db=self.default_dbs.redis_db,
            reducer_job_lifetime=30,  # 30 sec
            reducer_no_job_sleep_time=1,  # 1 sec
        )

        if use_booster:
            if booster is not None:
                self.booster = booster
            else:
                self.booster = sockets.SocketBooster(self)
        else:
            self.booster = None

    def run(self, steps=None, die_on_error=True, die_when_empty=False):
        if steps is None:
            steps = self.get_workers_steps()

        return workers.process(self,
                               *steps,
                               die_on_error=die_on_error,
                               die_when_empty=die_when_empty)

    def run_booster(self, steps=None, die_on_error=True, die_when_empty=False):
        if self.booster is None:
            raise RuntimeError("Booster is not enabled. Set use_booster=True "
                               "in app initialization.")
        if steps is None:
            steps = self.get_workers_steps()

        self.booster.process(steps,
                             die_on_error=die_on_error,
                             die_when_empty=die_when_empty)

    def run_reducer(self, reducer_step):
        self.reducer_engine.process(reducer_step)

    def just_do_it(self, workers_count, *args, _warning=True, **kwargs):
        if _warning:
            print("You are using python multiprocessing for workers")
        return simple_multiprocessing(self,
                                      workers_count,
                                      *args,
                                      steps=self.get_workers_steps(),
                                      **kwargs)

    def load_config(self, config_object):
        self.config = config_object
        self.init_dbs(config_object)

    def init_dbs(self, config):
        self.default_dbs = DBs(config)

    def get_workers_steps(self):
        return list(filter(lambda step: step.as_worker, self.steps.values()))

    def get_reducers_steps(self):
        return list(filter(lambda step: isinstance(step, ReducerStep),
                           self.steps.values()))

    def register_step(self, step):
        if str(step) in self.steps:
            raise RuntimeError("Step '%s' already exists!" % str(step))

        self.steps[step.step_key()] = step
        if step.as_worker:
            self.worker_engine.register_worker(step)

    def add_job(self, step, data, skip_booster=False, **kwargs):
        if self.booster and not skip_booster:
            self.booster.send_job(step, data, **kwargs)
        else:
            self.worker_engine.add_job(step, data, **kwargs)

    def step(self, next_step, as_worker=False, wait_result=False,
             unique_id=None, save_result=False, name=None):
        """
        Step decorator which initialize Step object, and register Step
        inside stepist


        :param next_step: next Step instance
        :param as_worker: True if it should be distribute
        :param wait_result: allow to return results in previous step
        :return:
        """

        def _wrapper(handler):
            step = Step(self,
                        handler,
                        next_step,
                        as_worker=as_worker,
                        unique_id=unique_id,
                        wait_result=wait_result,
                        save_result=save_result,
                        name=name)

            return step

        return _wrapper

    def reducer_step(self):
        """
        ReducerStep decorator. We need this for aggregate all jobs results into one
        step. And also register step in global step list.

        In args you will get iterator which allow you go through all jobs results
        and process it.

        For example you can paste everything into AI model

        :return: ReducerStep instance
        """

        def _wrapper(handler):
            step = ReducerStep(self, handler)

            self.register_step(step)
            return step

        return _wrapper

    def factory_step(self, next_step, as_worker=False):
        """
        Factory step decorator. If your step decorated by this function - your
        step should return iterator, and each item from this iter will be added
        to next step.

        :param next_step: Step instance
        :param as_worker: True if it should be distribute
        :return:
        """

        def _wrapper(handler):
            step = Step(self,
                        handler,
                        next_step,
                        as_worker=as_worker,
                        wait_result=False)

            step.set_factory(FactoryStep(step))

            self.register_step(step)
            return step

        return _wrapper

    def set_verbose(self, verbose):
        self.verbose = verbose
