#!/usr/bin/env python
# encoding: utf-8

from Flask.ext.script import Manager
from clinstat.app import app

manager = Manager(app)
app.config['DEBUG'] = True

if __name__ == '__main__':
    manager.run()
