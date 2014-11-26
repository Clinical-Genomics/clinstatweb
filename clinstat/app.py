#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals, absolute_import

import os

from flask import Flask
from werkzeug.utils import import_string

from .settings import DevelopmentConfig

class AppFactory(object):

    def __init__(self):
        super(AppFactory, self).__init__()

    def __call__(self, app_name=None, config=None, **kwargs):
        # set up Flask instance
        self.app_config = config
        self.app = Flask(app_name or DevelopmentConfig.PROJECT, instance_relative_config=True, **kwargs)

        # config
        self._configure_app()

        # set up blueprints
        self._register_blueprints()

        # set up extensions: db, ...
        self._bind_extensions()

        return self.app

    def _get_imported_stuff_by_path(self, path):
        module_name, object_name = path.rsplit('.', 1)
        module = import_string(module_name)

        return module, object_name

    def _configure_app(self, config_obj=None):
        """configure the app in different ways"""
        # http://flask.pocoo.org/docs/api/#configuration
        self.app.config.from_object(config_obj or DevelopmentConfig)

        # user custom config
        # http://flask.pocoo.org/docs/config/#instance-folders
        default_config = os.path.join(self.app.instance_path,
                                      "%s.cfg" % self.app.name)
        self.app.config.from_pyfile(self.app_config or default_config, silent=True)

    def _register_blueprints(self):
        for blueprint_path in self.app.config.get('BLUEPRINTS', []):
            module, object_name = self._get_imported_stuff_by_path(blueprint_path)

        if hasattr(module, object_name):
            self.app.register_blueprint(getattr(module, object_name))
        else:
            raise NoBlueprintException("No %s blueprint found" % object_name)

    def _bind_extensions(self):
        for ext_path in self.app.config.get('EXTENSIONS', []):
            module, object_name = self._get_imported_stuff_by_path(ext_path)

        if not hasattr(module, object_name):
            raise NoExtensionException("No %s extension found" % object_name)

        extension = getattr(module, object_name)

        if getattr(extension, 'init_app', False):
           extension.init_app(self.app)
        else:
           extension(self.app)

if __name__ == '__main__':
    app.run()
