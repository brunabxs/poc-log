#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import os

from kombu import Queue, Exchange

CONFIG_DIR = '/etc/tivitcloud-log'

LOCAL_CONFIG_DIR = os.path.join(
    os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
    'config/tivitcloud-log'
)

if os.path.exists(LOCAL_CONFIG_DIR):
    CONFIG_DIR = LOCAL_CONFIG_DIR

CONFIG_FILE = '{}/log.ini'.format(CONFIG_DIR)

if not os.path.exists(CONFIG_FILE):
    raise Exception('CONFIG FILE NOT FOUND: "{}".'.format(CONFIG_FILE))

config_ini = configparser.ConfigParser()
config_ini.read(CONFIG_FILE)


class Configuration(object):
    ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    BROKER_USE_SSL = config_ini.getboolean('amqp', 'verify_ssl')

    BROKER_URL = 'amqp://{}:{}@{}/{}'.format(
        config_ini.get('amqp', 'username'),
        config_ini.get('amqp', 'password'),
        config_ini.get('amqp', 'endpoint'),
        config_ini.get('amqp', 'virtual_host'))

    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'

    CELERYD_LOG_FILE = '/var/log/apps/celery/%n.log'
    CELERYD_PID_FILE = '/tmp/celeryd@%n.pid'

    CELERYD_PREFETCH_MULTIPLIER = 1
    CELERY_DISABLE_RATE_LIMITS = True

    CELERYD_CONCURRENCY = 5

    CELERYD_TASK_TIME_LIMIT = 900
    CELERYD_TASK_SOFT_TIME_LIMIT = 850

    CELERY_QUEUES = (
        Queue(
            'log.process',
            Exchange('log.process'),
            routing_key='log.process'),
    )

    ONCE = {
        'backend': 'celery_once.backends.Redis',
        'settings': {
            'url': 'redis://{}:{}/{}'.format(
                config_ini.get('cache', 'host'),
                config_ini.get('cache', 'port'),
                config_ini.get('cache', 'database'),
            ),
            'default_timeout': config_ini.get('cache', 'timeout')
        }
    }
    #
    # LOG_FILENAME = '/var/log/apps/tivitcloud-log.log'
    #
    # LOG_TAG = 'ACCOUNTANT'
    #
    # LOG_LEVEL = logging.DEBUG
    # LOG_FORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    CACHE_TYPE = 'redis'
    CACHE_KEY_PREFIX = config_ini.get('cache', 'prefix')
    CACHE_DEFAULT_TIMEOUT = config_ini.get('cache', 'timeout')
    CACHE_REDIS_HOST = config_ini.get('cache', 'host')
    CACHE_REDIS_PORT = config_ini.get('cache', 'port')
    CACHE_REDIS_DB = config_ini.get('cache', 'database')

    VERIFY_SSL = False
