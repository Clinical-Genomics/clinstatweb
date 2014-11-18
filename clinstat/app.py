#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from clinstat.models import Base


class AppFactory(object):

    def __init__(self):
        super(AppFactory, self).__init__()

    def __call__(self, app_name=None, config=None, **kwargs):
        self.app_config = config
        self.app = Flask(app_name or __name__, instance_relative_config=True, **kwargs)

        self.app.config.from_pyfile(config)

        return self.app

if __name__ == '__main__':
    app.run()
