#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager

from log import commands
from log.app import create_app

app = create_app()
manager = Manager(app)


@manager.command
def process():
    commands.process_by_command()

if __name__ == "__main__":
    manager.run()
