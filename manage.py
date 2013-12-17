#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Standard libs
import os

# Third party libs
from flask.ext.script import Manager, Server

# Our libs
from upvotebay.app import create_app
from upvotebay.settings import DevConfig, ProdConfig

# Constants
DEFAULT_PORT = 8080

def _create_app():
    env = os.getenv('UPVOTEBAY_ENV', 'dev')

    if env.lower() == 'prod':
        app = create_app(ProdConfig)
    else:
        app = create_app(DevConfig)

    return app

# Initialize Manager
manager = Manager(_create_app())

# Built-in commands
manager.add_command('runserver', Server(host='0.0.0.0',
                                        port=os.getenv('PORT', DEFAULT_PORT)))

if __name__ == '__main__':
    manager.run()
