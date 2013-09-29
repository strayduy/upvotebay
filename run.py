#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Standard libs
import os

# Our libs
from upvotebay import main

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    main.app.run(port=port)
