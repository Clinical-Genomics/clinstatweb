#!/usr/bin/env python
# encoding: utf-8

from flask.ext.script import Manager, Server

from clinstat.app import AppFactory
from clinstat.extensions import ctx

app = AppFactory()
manager = Manager(app)

  
class SecureServer(Server):
  """Enable conditional setup of SSL context.

  Takes effect during ``app.run()`` execution depending on DEBUG mode.
  """
  def __call__(self, app, *args, **kwargs):

    if not app.config.get('SSL_MODE'):
      # Remove SSL context
      del self.server_options['ssl_context']

    # Run the original ``__call__`` function
    super(SecureServer, self).__call__(app, *args, **kwargs)

manager.add_command('serve', SecureServer(ssl_context=ctx, host='0.0.0.0'))
manager.add_option(
    '-c', '--config', dest='config', required=False, help='Config file path')

if __name__ == '__main__':
    manager.run()
