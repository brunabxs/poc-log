#!/usr/bin/env python
# -*- coding: utf-8 -*-

from log.app import log
from log.tasks import task_process_parent


def process_by_command():
    log.debug('Send task_process_parent to process')
    task_process_parent.delay()
    log.debug('Sent task_process_parent')
