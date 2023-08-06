# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from pytest import raises
from _sadm.errors import EnvError

def test_configure_disabled(testing_plugin):
	p = testing_plugin('docker', cfgdir = '.', cfgfn = 'config-disable.ini')
	p.configure()

def test_compose_name_empty(testing_plugin):
	p = testing_plugin('docker', cfgdir = '.', cfgfn = 'compose-name-error.ini')
	with raises(EnvError, match = 'docker-compose name is empty'):
		p.configure()

def test_compose_path_empty(testing_plugin):
	p = testing_plugin('docker', cfgdir = '.', cfgfn = 'compose-path-error.ini')
	with raises(EnvError, match = 'docker-compose:testing path is empty'):
		p.build()
