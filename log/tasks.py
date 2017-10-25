#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid

import flask
from celery.exceptions import SoftTimeLimitExceeded
from celery_once import AlreadyQueued, QueueOnce

from log.app import celery, log
from log.backend import process


class NewBaseTask(QueueOnce):
    def apply_async(self, args=None, kwargs=None, **options):
        if 'headers' not in kwargs or kwargs['headers'] is None:
            kwargs['headers'] = {}

        if not getattr(flask.g, 'request_id', None):
            flask.g.request_id = str(uuid.uuid4())
        kwargs['headers']['safe_request_id'] = getattr(flask.g, 'request_id')

        return super(NewBaseTask, self).apply_async(*args, **kwargs, **options)


@celery.task(name='log.process_parent',
             queue='log.process',
             soft_time_limit=20,
             base=NewBaseTask, once={'timeout': 60})
def task_process_parent():
    log.debug('Process')
    try:
        process()

        log.debug('Send task_process_child to process')
        task_process_child.delay(12)
        log.debug('Sent task_process_child')

        log.debug('End process')
    except AlreadyQueued:
        log.error('Already queued')
    except SoftTimeLimitExceeded as error:
        log.error('Soft time limit exceeded')
    except Exception as error:
        log.error('Generic error', error)


@celery.task(name='log.process_child',
             queue='log.process',
             soft_time_limit=20,
             base=NewBaseTask, once={'timeout': 60})
def task_process_child(argument):
    log.debug('Process')
    try:
        process()

        log.debug('End process')
    except AlreadyQueued:
        log.error('Already queued')
    except SoftTimeLimitExceeded as error:
        log.error('Soft time limit exceeded')
    except Exception as error:
        log.error('Generic error')


@celery.task(name='log.process_api',
             queue='log.process',
             soft_time_limit=20,
             base=NewBaseTask, once={'timeout': 60})
def task_process_api():
    log.debug('Process')
    try:
        process()

        log.debug('End process')
    except AlreadyQueued:
        log.error('Already queued')
    except SoftTimeLimitExceeded as error:
        log.error('Soft time limit exceeded')
    except Exception as error:
        log.error('Generic error')
