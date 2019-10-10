# -*- coding:utf8 -*-
import redis


class Config(object):
    """配置信息"""

    SECRET_KEY = "xasddasdcasdasd"

    # 数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/ihome"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # flask-session配置
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # 对cookies中的session_id进行隐藏
    PERMANENT_SESSION_LIFETIME = 24 * 3600  # session数据的有效期，单位秒


class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境的配置信息"""
    pass


# 建立名字和类的映射关系
config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}
