# encoding: utf-8

from __future__ import absolute_import, unicode_literals

######################
# Flask-DebugToolbar #
######################
from flask.ext.debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension()

####################
# Flask-SQLAlchemy #
####################
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

