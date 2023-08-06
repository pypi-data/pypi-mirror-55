# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import bottle

from _sadm import log
from _sadm.devops.wapp.auth.config import AuthConfig
from _sadm.devops.wapp.auth.error import AuthError

__all__ = ['AuthSSLCert']

class AuthSSLCert(AuthConfig):

	def __init__(self, cfg):
		super().__init__(cfg)
		self.cfg = cfg['devops']
		self.auth = cfg['devops.auth']
		self._header = self.cfg.get('auth.header', fallback = 'X-Client-Fingerprint')
		self._tokenHeader = self.cfg.get('auth.token.header', fallback = 'X-Auth-Token')

	def check(self, req):
		log.debug('check sslcert')
		# https scheme
		scheme = req.headers.get('X-Forwarded-Proto', 'none')
		if scheme != 'https':
			raise AuthError('auth request not from an ssl proxy')
		# auth token from request headers
		htok = req.headers.get(self._tokenHeader, None)
		if htok is None:
			raise AuthError('auth token not found')
		htok = self.digest(htok.strip())
		# check token from config
		tok = self.cfg.get('auth.token', fallback = None)
		if tok is None:
			raise AuthError('auth token not configured')
		tok = tok.strip()
		if htok != tok:
			log.debug("header token: %s" % htok)
			raise AuthError('invalid auth token')
		# get user identification from request headers
		uid = req.headers.get(self._header, None)
		if uid is None:
			raise AuthError('auth user id not found')
		return uid

	def login(self, req):
		log.debug('login sslcert')
		username = req.forms.get('username')
		if not username:
			raise bottle.HTTPError(401, 'username not provided')
		uid = self.check(req)
		x = self.auth.get(username, fallback = None)
		if x is None:
			raise AuthError("invalid username: %s" % username)
		uid = self.digest(uid.strip())
		if x != uid:
			raise AuthError("user %s: invalid id" % username)
		return username
