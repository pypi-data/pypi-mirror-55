# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import bottle

from _sadm import log
from _sadm.devops.wapp.auth.auth import WebappAuth, AuthError

__all__ = ['AuthPlugin']

class AuthPlugin(object):
	api = 2
	name = 'sadm.devops.auth'

	def __init__(self, config):
		self.config = config

	def setup(self, wapp):
		log.debug('setup')
		self.auth = WebappAuth(self.config)

	def apply(self, callback, ctx):
		log.debug("apply for rule: %s" % ctx.rule)
		def wrapper(*args, **kwargs):
			log.debug('apply.wrapper')
			user = None
			autherr = None
			try:
				log.debug('user auth check')
				user = self.auth.check(bottle.request)
			except AuthError as err:
				autherr = err
			if autherr is None:
				kwargs['user'] = user
				resp = callback(*args, **kwargs)
				return resp
			else:
				log.error("auth error: %s" % autherr)
				return self.auth.error()
		return wrapper
