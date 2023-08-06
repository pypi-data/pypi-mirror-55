# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import bottle

from pytest import raises
from unittest.mock import Mock

from _sadm.devops.wapp.auth import auth
from _sadm.devops.wapp.auth.config import AuthConfig
from _sadm.devops.wapp.auth.error import AuthError
from _sadm.devops.wapp.user import WebappUser
from _sadm.devops.wapp.view import view

def test_init(devops_wapp):
	wapp = devops_wapp('auth')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		assert isinstance(wa._auth, AuthConfig)

def test_init_error(devops_wapp):
	wapp = devops_wapp('auth')
	with wapp.mock() as ctx:
		ctx.config.set('devops', 'auth', 'testing.invalid')
		with raises(RuntimeError, match = 'invalid auth type: testing.invalid'):
			auth.WebappAuth(ctx.config)

def test_error(devops_wapp):
	wapp = devops_wapp('auth')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		with raises(bottle.HTTPResponse) as exc:
			wa.error()
		wapp.checkRedirect(exc, 302, view.url('user.login'))

def test_user(devops_wapp):
	wapp = devops_wapp('auth')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		sess, _ = wapp.mock_sess(wa, '01234567')
		u = wa._user(sess)
		assert isinstance(u, WebappUser)
		assert u.name == 'testing'
		assert u.sess.id == '01234567'
		assert u.sess.user == 'testing'
		assert u.email is None

def test_user_options(devops_wapp):
	wapp = devops_wapp('auth')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		sess, _ = wapp.mock_sess(wa, '01234567', user = 'tuser')
		u = wa._user(sess)
		assert isinstance(u, WebappUser)
		assert u.name == 'tuser'
		assert u.sess.id == '01234567'
		assert u.sess.user == 'tuser'
		assert u.email == 'tuser@testing.com'
		assert u._info.get('testing', None) is None

def test_user_disabled(devops_wapp):
	wapp = devops_wapp('auth')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		sess, _ = wapp.mock_sess(wa, '01234567', user = 'tuser_disable')
		with raises(AuthError, match = 'user tuser_disable: disabled'):
			wa._user(sess)

def test_check(devops_wapp):
	wapp = devops_wapp('auth')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		sess, req = wapp.mock_sess(wa, '01234567')
		u = wa.check(req)
		assert isinstance(u, WebappUser)

def test_check_sess_error(devops_wapp):
	wapp = devops_wapp('auth')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		req = wapp.mock_req(None)
		with raises(AuthError, match = 'user session not found'):
			wa.check(req)

def test_login_user_error(devops_wapp):
	wapp = devops_wapp('auth')
	with wapp.mock() as ctx:
		wa = auth.WebappAuth(ctx.config)
		sess, req = wapp.mock_sess(wa, '01234567', user = 'tuser')
		wa._auth.login = Mock(return_value = None)
		with raises(AuthError, match = 'could not get the username'):
			wa.login(req, '01234567')
