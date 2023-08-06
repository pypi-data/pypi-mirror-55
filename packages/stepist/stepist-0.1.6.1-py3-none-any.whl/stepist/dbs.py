import redis

from stepist import app_config


class DBs:

    def __init__(self, config):
        self.config = config
        self.redis_db = init_redis(**config.redis_kwargs)
        self.redis_stats = init_redis(**config.redis_stats_kwargs)

    def reset(self):
        return self.__class__(self.config)


def init_redis(**redis_kwargs):
    return redis.Redis(**redis_kwargs)
