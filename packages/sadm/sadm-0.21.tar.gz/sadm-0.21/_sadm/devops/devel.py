# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import bottle

from _sadm.devops.wapp import wapp

__all__ = ['application']

bottle.DEBUG = True

application = wapp.init()
