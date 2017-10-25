#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid

from celery import Celery
from flask import Flask
from logbook import Logger

from logbook import NestedSetup, Processor, RotatingFileHandler

celery = Celery(__name__)
log = Logger('Logbook')


def inject_information(record):
    from celery import current_task
    import flask

    if current_task:
        record.extra['task_id'] = current_task.request.id
        record.extra['task_name'] = current_task.name
        if current_task.request.kwargs:
            record.extra['task_kwargs'] = current_task.request.kwargs
        if current_task.request.parent_id:
            record.extra['task_parent_id'] = current_task.request.parent_id
        record.extra['queue_name'] = current_task.queue
        record.extra['request_id'] = current_task.request.safe_request_id

    if flask.has_request_context():
        if not getattr(flask.g, 'request_id', None):
            flask.g.request_id = str(uuid.uuid4())
        record.extra['request_id'] = getattr(flask.g, 'request_id')


def create_app(settings_override={}):
    app = Flask(__name__)
    app.config.from_object('log.settings.Configuration')
    app.config.update(settings_override)

    celery.conf.update(app.config)

    # Se houver a necessidade de adicionar ao log mais informações
    # é necessário incluir novos processors ou trabalhar melhor o record.extra
    setup = NestedSetup([
        Processor(inject_information),
        RotatingFileHandler('/var/log/apps/tivitcloud-log.log',
                            format_string=u'[{record.time:%Y-%m-%d %H:%M:%S.%f%z}] '
                                          '{record.level_name}: {record.channel}: {record.message}:'
                                          '{record.extra}')
    ])
    setup.push_application()

    from log.api.base import apiv1
    app.register_blueprint(apiv1)

    return app
