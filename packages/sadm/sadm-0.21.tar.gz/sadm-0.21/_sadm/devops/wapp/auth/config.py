# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import bottle

from hashlib import sha256

from _sadm import log
from _sadm.devops.wapp.auth.error import AuthError

__all__ = ['AuthConfig']

class AuthConfig(object):

	def __init__(self, cfg):
		self.cfg = cfg['devops.auth']

	def digest(self, s):
		h = sha256(s.encode('utf-8'))
		return h.hexdigest()

	def login(self, req):
		log.debug('login')
		username = req.forms.get('username')
		password = req.forms.get('password')
		if not username:
			raise bottle.HTTPError(401, 'username not provided')
		if not password:
			raise bottle.HTTPError(401, 'user password not provided')
		p = self.cfg.get(username, fallback = None)
		if p is None:
			raise AuthError("invalid username: %s" % username)
		h = self.digest(password)
		if h != p:
			raise AuthError("user %s: invalid password" % username)
		return username
