# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from unittest.mock import Mock

from _sadm.devops.wapp.view import index

def test_handle(devops_wapp):
	wapp = devops_wapp()
	with wapp.mock() as ctx:
		bup = Mock()
		bup._repos = index._repos
		try:
			repos = object()
			index._repos = Mock(return_value = repos)
			index.handle(user = None)
		finally:
			del index._repos
			index._repos = bup._repos
		ctx.tpl.parse.assert_called_with('index', repos = repos, user = None)
