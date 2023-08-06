# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import bottle
import re

from collections import deque
from unittest.mock import call

from _sadm.devops.wapp import errors

def test_init(devops_wapp):
	re_error_init = re.compile(r'^call\(\)\(<function init.<locals>.(error_\d+) at 0x')
	wapp = devops_wapp()
	with wapp.mock() as ctx:
		errors.init(ctx.wapp)
		x = deque()
		for c in ctx.wapp.error.mock_calls:
			m = re_error_init.match(str(c))
			if m:
				x.append(call()(m.group(1)))
			else:
				x.append(c)
		assert list(x) == [
			call(400),
			call()('error_400'),
			call(401),
			call()('error_401'),
			call(404),
			call()('error_404'),
			call(500),
			call()('error_500'),
		]

def test_handler(devops_wapp):
	wapp = devops_wapp()
	with wapp.mock() as ctx:
		err = ctx.mock.error
		err.args = []
		err.status_code = 999
		err.status = '999 testing'
		errors._handler(err)
		ctx.tpl.parse.assert_called_with('errors', error = err)

def test_handler_debug(devops_wapp):
	wapp = devops_wapp()
	with wapp.mock() as ctx:
		err = ctx.mock.error
		err.args = ['arg0', 'arg1', 'arg2', 'arg3']
		err.status_code = 999
		err.status = '999 testing'
		errors._handler(err)
		ctx.tpl.parse.assert_called_with('errors', error = err)
