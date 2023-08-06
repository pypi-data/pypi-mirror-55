# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import bottle

from contextlib import contextmanager
from pytest import raises
from unittest.mock import Mock

from _sadm.devops.wapp.auth.error import AuthError
from _sadm.devops.wapp.view import view
from _sadm.devops.wapp.view.user import auth

@contextmanager
def mock_session(wapp):
	bup = Mock()
	bup.session = auth.session
	with wapp.mock() as ctx:
		try:
			ctx.session = ctx.mock.session
			ctx.session.cookie.return_value = '01234567'
			auth.session = ctx.session
			ctx.auth = ctx.mock.auth
			yield ctx
		finally:
			del auth.session
			auth.session = bup.session

def test_login(devops_wapp):
	wapp = devops_wapp()
	with mock_session(wapp) as ctx:
		ctx.session.cookie.return_value = None
		auth.login(auth = ctx.auth)
		req = bottle.request
		resp = bottle.response
		ctx.session.cookie.assert_called_with(req)
		ctx.session.new.assert_called_with(resp)
		ctx.tpl.parse.assert_called_with('user/login', auth = ctx.auth)
		assert ctx.auth.mock_calls == []

def test_auth_check(devops_wapp):
	wapp = devops_wapp()
	with mock_session(wapp) as ctx:
		with raises(bottle.HTTPResponse) as resp:
			auth.login(auth = ctx.auth)
		wapp.checkRedirect(resp, 302, view.url('index'))
		req = bottle.request
		resp = bottle.response
		ctx.auth.check.assert_called_with(req)
		assert ctx.tpl.parse.mock_calls == []
		ctx.session.cookie.assert_called_with(req)
		assert ctx.session.new.mock_calls == []

def test_auth_error(devops_wapp):
	wapp = devops_wapp()
	with mock_session(wapp) as ctx:
		ctx.auth.check.side_effect = AuthError('testing')
		auth.login(auth = ctx.auth)
		req = bottle.request
		req = bottle.request
		resp = bottle.response
		ctx.auth.check.assert_called_with(req)
		ctx.session.cookie.assert_called_with(req)
		ctx.tpl.parse.assert_called_with('user/login', auth = ctx.auth)

def test_auth_exception(devops_wapp):
	wapp = devops_wapp()
	with mock_session(wapp) as ctx:
		ctx.auth.check.side_effect = RuntimeError('testing')
		with raises(RuntimeError, match = 'testing'):
			auth.login(auth = ctx.auth)
		assert ctx.tpl.parse.mock_calls == []

def test_login_post(devops_wapp):
	wapp = devops_wapp()
	with mock_session(wapp) as ctx:
		with raises(bottle.HTTPResponse) as resp:
			auth.loginPost(auth = ctx.auth)
		req = bottle.request
		ctx.session.cookie.assert_called_with(req)
		ctx.auth.login.assert_called_with(req, '01234567')
		wapp.checkRedirect(resp, 302, view.url('index'))

def test_login_post_no_session_cookie(devops_wapp):
	wapp = devops_wapp()
	with mock_session(wapp) as ctx:
		ctx.session.cookie.return_value = None
		with raises(bottle.HTTPResponse) as resp:
			auth.loginPost(auth = ctx.auth)
		req = bottle.request
		ctx.session.cookie.assert_called_with(req)
		wapp.checkRedirect(resp, 302, view.url('user.login'))

def test_login_post_auth_error(devops_wapp):
	wapp = devops_wapp()
	with mock_session(wapp) as ctx:
		ctx.auth.login.side_effect = AuthError('testing')
		resp = auth.loginPost(auth = ctx.auth)
		assert isinstance(resp, bottle.HTTPError)
		assert resp.status_code == 401
		req = bottle.request
		ctx.session.cookie.assert_called_with(req)
		ctx.auth.login.assert_called_with(req, '01234567')
