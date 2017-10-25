#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

from log.app import log
from log.tasks import task_process_api

apiv1 = Blueprint('apiv1', __name__, url_prefix='/api/v1')
RESPONSE_HEADERS = {'Content-Type': 'application/json'}


@apiv1.route('/')
def get_apiv1():
    log.debug('Send task_process_api to process')
    task_process_api.delay()
    log.debug('Sent task_process_api')
    return 'API v1', 200, RESPONSE_HEADERS
