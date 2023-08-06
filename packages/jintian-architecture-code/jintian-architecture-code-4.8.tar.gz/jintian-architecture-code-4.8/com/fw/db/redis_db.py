import time

import redis
import threading

from com.fw.base.base_exception import BaseException
from com.fw.base.base_log import logger
from com.fw.system.red_conf import system_conf
from com.fw.utils.id_util import IDUtils


class RedisDB(object):

    def __init__(self):
        self.init_pool()

    def init_pool(self):
        if not system_conf.has_group('environment'):
            raise BaseException("没有配置数据库环境...")
        version = system_conf.get_value('environment', 'version')

        key = 'redis' + "_" + version

        if not system_conf.has_group(key):
            logger.warn("-----WARN：没有配置redis -------")
            return

        try:
            password = system_conf.get_value(key, "password")
        except Exception as e:
            logger.warn("没有配置redis密码", e)
            self.redis_pool = redis.ConnectionPool(host=system_conf.get_value(key, 'host'),
                                                   port=system_conf.get_value(key, 'port'),
                                                   max_connections=60, socket_connect_timeout=3)
        else:
            self.redis_pool = redis.ConnectionPool(host=system_conf.get_value(key, 'host'),
                                                   port=system_conf.get_value(key, 'port'), password=password,
                                                   max_connections=60, socket_connect_timeout=3)

        self.connection_client = redis.Redis(connection_pool=self.redis_pool)

        self.connection_client.get_str = self.get_str
        logger.info("------ redis 初始化成功 ------")

    def get_str(self, name):
        return str(self.connection_client.get(name), encoding="utf8")


redis = RedisDB()

redis_db = redis.connection_client
