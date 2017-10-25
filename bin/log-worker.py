#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log.app import celery, create_app # NOQA

app = create_app()
app.app_context().push()

from log import tasks  # NOQA
