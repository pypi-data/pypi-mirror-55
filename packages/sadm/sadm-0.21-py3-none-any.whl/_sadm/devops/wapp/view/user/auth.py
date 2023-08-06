# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import bottle

from _sadm import log
from _sadm.devops.wapp import cfg
from _sadm.devops.wapp.auth.auth import WebappAuth, AuthError
from _sadm.devops.wapp.session import session
from _sadm.devops.wapp.tpl import tpl
from _sadm.devops.wapp.view import view

__all__ = ['login', 'loginPost']

def login(auth = None):
	log.debug('login')
	req = bottle.request
	resp = bottle.response
	if auth is None: # pragma: no cover
		auth = WebappAuth(cfg.config)
	sessid = session.cookie(req)
	if not sessid:
		session.new(resp)
	else:
		try:
			auth.check(req)
			bottle.redirect(view.url('index'))
		except AuthError as err:
			# if there was an auth error we show the login form
			log.debug("auth error: %s" % err)
	return tpl.parse('user/login', auth = auth)

def loginPost(auth = None):
	log.debug('login post')
	req = bottle.request
	if auth is None: # pragma: no cover
		auth = WebappAuth(cfg.config)
	sessid = session.cookie(req)
	if not sessid:
		log.error('session cookie not found')
		bottle.redirect(view.url('user.login'))
	try:
		auth.login(req, sessid)
		log.debug('login done')
	except AuthError as err:
		log.error("login: %s" % err)
		return bottle.HTTPError(401, str(err))
	log.debug('redirect')
	bottle.redirect(view.url('index'))
