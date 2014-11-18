#!/usr/bin/env python
# encoding: utf-8

from flask.ext.script import Manager
from clinstat.app import AppFactory

app = AppFactory()
manager = Manager(app)

manager.add_option(
    '-c', '--config', dest='config', required=False, help='Config file path')

if __name__ == '__main__':
    manager.run()
