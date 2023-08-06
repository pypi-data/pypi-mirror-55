# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import bottle

from _sadm import log
from _sadm.devops.wapp.auth.config import AuthConfig
from _sadm.devops.wapp.auth.error import AuthError
from _sadm.devops.wapp.auth.sslcert import AuthSSLCert
from _sadm.devops.wapp.session.session import WebappSession
from _sadm.devops.wapp.user import WebappUser, userOptions
from _sadm.devops.wapp.view import view

__all__ = ['WebappAuth', 'AuthError']

class WebappAuth(object):
	_auth = None

	def __init__(self, config):
		if not config.has_section('devops.auth'):
			config.add_section('devops.auth')
		self._cfg = config
		self.sess = WebappSession()
		self.type = config.get('devops', 'auth', fallback = 'config')
		log.debug("init %s manager" % self.type)
		if self.type == 'config':
			self._auth = AuthConfig(config)
		elif self.type == 'sslcert':
			self._auth = AuthSSLCert(config)
		else:
			raise RuntimeError("invalid auth type: %s" % self.type)

	def error(self):
		log.info('login error, redirect to user login page')
		bottle.redirect(view.url('user.login'))

	def _user(self, sess):
		info = {}
		sect = "devops.user:%s" % sess.user
		if self._cfg.has_section(sect):
			dis = self._cfg.getboolean(sect, 'disable', fallback = False)
			if dis:
				raise AuthError("user %s: disabled" % sess.user)
			for opt in self._cfg.options(sect):
				if userOptions.get(opt, False):
					info[opt] = self._cfg.get(sect, opt)
		return WebappUser(sess.user, sess = sess, info = info)

	def check(self, req):
		sess = self.sess.check(req)
		if not sess:
			raise AuthError('user session not found')
		return self._user(sess)

	def login(self, req, sessid):
		username = self._auth.login(req)
		if not username:
			err = AuthError('could not get the username')
			log.debug("%s" % err)
			raise err
		sess = self.sess.save(sessid, username)
		log.info("user login: %s" % username)
		return self._user(sess)
