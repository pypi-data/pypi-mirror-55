# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import bottle

from datetime import datetime
from pytest import raises
from secrets import token_urlsafe, token_hex

from _sadm.devops.wapp.session import session

def test_secret_token(devops_wapp):
	assert session._secret is None
	wapp = devops_wapp()
	with wapp.mock() as ctx:
		assert isinstance(session._secret, str)
		x = token_hex(session._tokenSize)
		# check we have the correct size on database VARCHAR for the session id
		assert len(x) == session._tokenSize * 2
		session._secret = None
		resp = ctx.mock.response
		with raises(RuntimeError, match = 'session module not initialized'):
			session.new(resp)
		req = ctx.mock.request
		with raises(RuntimeError, match = 'session module not initialized'):
			session.cookie(req)
	assert session._secret is None

def test_new(devops_wapp):
	wapp = devops_wapp()
	with wapp.mock() as ctx:
		resp = ctx.mock.resp
		session.new(resp, sid = 'testing')
		resp.set_cookie.assert_called_with('sadm_devops_session', 'testing',
			secret = session._secret, path = '/', httponly = True)

def test_cookie(devops_wapp):
	wapp = devops_wapp()
	with wapp.mock() as ctx:
		req = ctx.mock.request
		req.get_cookie.return_value = 'testing'
		c = session.cookie(req)
		assert c == 'testing'
		req.get_cookie.assert_called_with('sadm_devops_session',
			secret = session._secret)

def test_save_check(devops_wapp):
	wapp = devops_wapp('session')
	with wapp.mock() as ctx:
		req = ctx.mock.request
		req.get_cookie.return_value = None
		s = session.WebappSession()
		retval = s.check(req)
		assert retval is None
		sess = s.save('tsid', 'testing')
		assert isinstance(sess, session.Session)
		assert sess.pk == 1
		assert sess.id == 'tsid'
		assert sess.user == 'testing'
		assert isinstance(sess.last, datetime)
		req.get_cookie.return_value = 'tsid'
		x = s.check(req)
		assert isinstance(x, session.Session)
		assert x.pk == 1
		assert x.id == 'tsid'
		assert x.user == 'testing'
		assert isinstance(x.last, datetime)
