# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from pytest import raises
from _sadm.errors import PluginError

def _new(new, cfgfn):
	return new('templates', cfgdir = '.', cfgfn = cfgfn)

def test_name_empty_error(testing_plugin):
	p = _new(testing_plugin, 'error-name-empty.ini')
	with raises(PluginError, match = 'template name is empty'):
		p.configure()

def test_src_notset_error(testing_plugin):
	p = _new(testing_plugin, 'error-src-notset.ini')
	with raises(PluginError, match = 'template testing src.path not set'):
		p.configure()

def test_dst_notset_error(testing_plugin):
	p = _new(testing_plugin, 'error-dst-notset.ini')
	with raises(PluginError, match = 'template testing dst.path not set'):
		p.configure()

def test_src_file_notfound(testing_plugin):
	p = _new(testing_plugin, 'error-src-notfound.ini')
	with raises(PluginError, match = 'template testing src.path testing.tpl: file not found'):
		p.configure()

def test_dst_file_notabs(testing_plugin):
	p = _new(testing_plugin, 'error-dst-notabs.ini')
	with raises(PluginError, match = 'template testing dst.path testing.txt: must be an absolute path'):
		p.configure()

def test_tpl_key_error(testing_plugin):
	p = _new(testing_plugin, 'error-tpl-key.ini')
	with raises(PluginError, match = "template testing key miss: 'tdata'"):
		p.build()
