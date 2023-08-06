# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from pytest import raises

from _sadm.devops.wapp.tpl import tpl

def test_init(devops_wapp):
	wapp = devops_wapp()
	with wapp.mock() as ctx:
		ctx.orig.tpl.parse('testing.html', tdata = None)
		ctx.bottle.template.assert_called_once()

def test_template(devops_wapp):
	wapp = devops_wapp()
	with wapp.mock() as ctx:
		t = tpl.Template('testing.html', {})
		assert t.name == 'testing.html'
		assert t.data == {'sadm': {'version': 'testing'}}

def test_tpl_error(devops_wapp):
	wapp = devops_wapp()
	with wapp.mock() as ctx:
		t = tpl.Template('testing.html', {'error': None})
		assert t.error is None
		x = object()
		t.data['error'] = x
		assert t.error is x

def test_tpl_getitem(devops_wapp):
	wapp = devops_wapp()
	with wapp.mock() as ctx:
		t = tpl.Template('testing.html', {'tdata': 'testing'})
		assert t['tdata'] == 'testing'

def test_tpl_get(devops_wapp):
	wapp = devops_wapp()
	with wapp.mock() as ctx:
		t = tpl.Template('testing.html', {'tdata': 'testing'})
		assert t.get('tdata') == 'testing'

def test_tpl_get_default(devops_wapp):
	wapp = devops_wapp()
	with wapp.mock() as ctx:
		t = tpl.Template('testing.html', {})
		assert t.get('tdata', 'testing') == 'testing'

def test_tpl_get_error(devops_wapp):
	wapp = devops_wapp()
	with wapp.mock() as ctx:
		t = tpl.Template('testing.html', {})
		with raises(KeyError, match = 'template testing.html: tdata'):
			t.get('tdata')
