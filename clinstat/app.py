#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.utils import import_string

from clinstat.models import Base

class AppFactory(object):

    def __init__(self):
        super(AppFactory, self).__init__()

    def __call__(self, app_name=None, config=None, **kwargs):
        # set up Flask instance
        self.app = Flask(app_name or __name__, instance_relative_config=True, **kwargs)

        # config
        self.app_config = config
        self.app.config.from_pyfile(config)

        # set up SQLAlchemy
        db = SQLAlchemy(self.app)
        db.Model = Base

        # set up blueprints
        self._register_blueprints()

        return self.app

    def _get_imported_stuff_by_path(self, path):
        module_name, object_name = path.rsplit('.', 1)
        module = import_string(module_name)

        return module, object_name

    def _register_blueprints(self):
        for blueprint_path in self.app.config.get('BLUEPRINTS', []):
            module, object_name = self._get_imported_stuff_by_path(blueprint_path)

        if hasattr(module, object_name):
            self.app.register_blueprint(getattr(module, object_name))
        else:
            raise NoBlueprintException("No %s blueprint found" % object_name)

if __name__ == '__main__':
    app.run()
