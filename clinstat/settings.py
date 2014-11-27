from __future__ import absolute_import, unicode_literals
import os


class BaseConfig(object):
  """docstring for BaseConfig"""
  PROJECT = 'clinstatweb'

  APP_DIR = os.path.abspath(os.path.dirname(__file__))  # this directory
  # get app root path (can also use flask_root_path) => ../../config.py
  PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

  DEBUG = False
  TESTING = False

  BLUEPRINTS = ['clinstat.core.core']

  EXTENSIONS = ['clinstat.extensions.toolbar',
                'clinstat.extensions.ssl',
                'clinstat.extensions.db']

class DevelopmentConfig(BaseConfig):
  """docstring for DefaultConfig"""
  DEBUG = True

  # Flask-DebugToolbar
  DEBUG_TB_ENABLED = True
  DEBUG_TB_INTERCEPT_REDIRECTS = False
  DEBUG_TB_PANELS = [
    'flask_debugtoolbar.panels.versions.VersionDebugPanel',
    'flask_debugtoolbar.panels.timer.TimerDebugPanel',
    'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
    'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
    'flask_debugtoolbar.panels.template.TemplateDebugPanel',
    'flask_debugtoolbar.panels.logger.LoggingPanel',
    'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
  ]


class TestConfig(BaseConfig):
  """docstring for TestConfig"""
  TESTING = True
  DEBUG = True
