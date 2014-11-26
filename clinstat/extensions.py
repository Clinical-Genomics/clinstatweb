# encoding: utf-8

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

################
# Flask-SSLify #
################
from flask_sslify import SSLify
from OpenSSL import SSL

# (ext lacks init_app...)
ctx = SSL.Context(SSL.SSLv23_METHOD)

def ssl(app):
# Setup SSL: http://flask.pocoo.org/snippets/111/
    ctx.use_privatekey_file(app.config.get('SSL_KEY_PATH'))
    ctx.use_certificate_file(app.config.get('SSL_CERT_PATH'))

    # https://github.com/kennethreitz/flask-sslify
    # Force SSL. Redirect all incoming requests to HTTPS.
    # Only takes effect when DEBUG=False
    return SSLify(app)
