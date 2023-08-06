# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import bottle

from pytest import raises

from _sadm.devops.wapp.auth import auth
from _sadm.devops.wapp.auth.error import AuthError
from _sadm.devops.wapp.user import WebappUser

def test_login_config(devops_wapp):
	wapp = devops_wapp('auth')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		sess, req = wapp.mock_sess(wa, '01234567', user = 'tuser')
		u = wa.login(req, '01234567')
		assert isinstance(u, WebappUser)
		assert u.name == 'tuser'

def test_login_user_error(devops_wapp):
	wapp = devops_wapp('auth')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		sess, req = wapp.mock_sess(wa, '01234567', user = 'tuser')
		del req.forms
		req.forms = {}
		with raises(bottle.HTTPError) as exc:
			wa.login(req, '01234567')
		wapp.checkException(exc, 401, 'username not provided')

def test_login_user_password_error(devops_wapp):
	wapp = devops_wapp('auth')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		sess, req = wapp.mock_sess(wa, '01234567', user = 'tuser')
		del req.forms
		req.forms = {'username': 'tuser'}
		with raises(bottle.HTTPError) as exc:
			wa.login(req, '01234567')
		wapp.checkException(exc, 401, 'user password not provided')

def test_login_invalid_user(devops_wapp):
	wapp = devops_wapp('auth')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		sess, req = wapp.mock_sess(wa, '01234567')
		with raises(AuthError, match = 'invalid username: testing'):
			wa.login(req, '01234567')

def test_login_invalid_user_password(devops_wapp):
	wapp = devops_wapp('auth')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		sess, req = wapp.mock_sess(wa, '01234567', user = 'tuser')
		req.forms['password'] = 'invalid.password'
		with raises(AuthError, match = 'user tuser: invalid password'):
			wa.login(req, '01234567')
