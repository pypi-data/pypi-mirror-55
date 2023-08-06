# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import bottle

from pytest import raises

from _sadm.devops.wapp.auth import auth
from _sadm.devops.wapp.auth.error import AuthError
from _sadm.devops.wapp.user import WebappUser

def test_login_sslcert(devops_wapp):
	wapp = devops_wapp('auth.sslcert')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		sess, req = wapp.mock_sess(wa, '01234567', user = 'testing')
		u = wa.login(req, '01234567')
		assert isinstance(u, WebappUser)
		assert u.name == 'testing'

def test_proxy_error(devops_wapp):
	wapp = devops_wapp('auth.sslcert')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		sess, req = wapp.mock_sess(wa, '01234567', user = 'testing')
		req.headers['X-Forwarded-Proto'] = 'testing'
		with raises(AuthError, match = 'auth request not from an ssl proxy'):
			wa.login(req, '01234567')

def test_token_error(devops_wapp):
	wapp = devops_wapp('auth.sslcert')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		sess, req = wapp.mock_sess(wa, '01234567', user = 'testing')
		req.headers['X-Auth-Token'] = None
		with raises(AuthError, match = 'auth token not found'):
			wa.login(req, '01234567')

def test_token_config_error(devops_wapp):
	wapp = devops_wapp('auth.sslcert')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		sess, req = wapp.mock_sess(wa, '01234567', user = 'testing')
		del ctx.config['devops']['auth.token']
		with raises(AuthError, match = 'auth token not configured'):
			wa.login(req, '01234567')

def test_token_invalid(devops_wapp):
	wapp = devops_wapp('auth.sslcert')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		sess, req = wapp.mock_sess(wa, '01234567', user = 'testing')
		req.headers['X-Auth-Token'] = 'invalid.token'
		with raises(AuthError, match = 'invalid auth token'):
			wa.login(req, '01234567')

def test_user_error(devops_wapp):
	wapp = devops_wapp('auth.sslcert')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		sess, req = wapp.mock_sess(wa, '01234567', user = 'testing')
		req.headers['X-Client-Fingerprint'] = None
		with raises(AuthError, match = 'auth user id not found'):
			wa.login(req, '01234567')

def test_login_user_error(devops_wapp):
	wapp = devops_wapp('auth.sslcert')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		sess, req = wapp.mock_sess(wa, '01234567', user = 'testing')
		req.forms['username'] = None
		with raises(bottle.HTTPError) as exc:
			wa.login(req, '01234567')
		wapp.checkException(exc, 401, 'username not provided')

def test_login_user_invalid(devops_wapp):
	wapp = devops_wapp('auth.sslcert')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		sess, req = wapp.mock_sess(wa, '01234567', user = 'tuser')
		with raises(AuthError, match = 'invalid username: tuser'):
			wa.login(req, '01234567')

def test_login_user_invalid_id(devops_wapp):
	wapp = devops_wapp('auth.sslcert')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		sess, req = wapp.mock_sess(wa, '01234567', user = 'testing')
		req.headers['X-Client-Fingerprint'] = 'invalid.user.id'
		with raises(AuthError, match = 'user testing: invalid id'):
			wa.login(req, '01234567')
