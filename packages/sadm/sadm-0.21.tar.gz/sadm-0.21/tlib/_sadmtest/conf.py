# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import pytest

from os import path, makedirs, unlink
from shutil import rmtree, move
from unittest.mock import Mock

__all__ = [
	'env_setup',
	'testing_env',
	'testing_plugin',
	'testing_profile',
	'testing_settings',
	'testing_cmd',
	'listen_wapp',
	'testing_webapp',
	'devops_wapp',
]

#
# logger
#

from _sadm import log

log._colored = False
log.init('quiet')
log.init = Mock()

#
# remove version autogen module
#

for n in ('_version.py', '_version_build.py'):
	fn = path.join('_sadm', n)
	if path.isfile(fn):
		unlink(fn)

#
# register testing plugins
#

import _sadmtest.plugin.testing

#
# config
#

from _sadm import cfg
cfg._cfgFile = path.join('tdata', 'sadm.cfg')

import _sadm.deploy
_sadm.deploy.cfgfile = path.join('tdata', 'deploy.cfg')

#
# testing profile
#

from _sadm.env import profile

@pytest.fixture
def testing_profile():
	def wrapper(name = 'testing'):
		return profile.Profile(name)
	return wrapper

#
# testing env
#

from _sadm import env

@pytest.fixture
def testing_env():
	def wrapper(name = 'testing', profile = 'testing'):
		e = env.Env(profile, name)
		_cleanEnv(e)
		return e
	return wrapper

#
# testing settings
#

@pytest.fixture
def testing_settings():
	envmod = env
	def wrapper(profile = 'testing', env = 'testing', cfgfile = None):
		if cfgfile is not None:
			cfgfile = path.join(profile, cfgfile)
		e = envmod.Env(profile, env)
		_cleanEnv(e)
		e.configure(cfgfile = cfgfile)
		return e.settings
	return wrapper

#
# testing env setup
#

from _sadm.env import action as envAction

@pytest.fixture
def env_setup():
	return _newEnv

def _newEnv(name = 'testing', profile = 'envsetup', configure = False,
	cfgfile = None, action = None, mkdirs = False, config = None):
	if action is not None:
		# configure is called from cmd.run
		configure = False
	e = env.Env(profile, name, config = config)
	_cleanEnv(e, mkdirs = mkdirs)
	if configure:
		e.configure(cfgfile = cfgfile)
	if action is not None:
		envAction.run(e, action)
	return e

def _cleanEnv(env, mkdirs = False):
	tmpdir = path.join('tdata', 'tmp')
	bdir = path.normpath(env.build.rootdir())
	pdir = path.realpath(path.join('tdata', env.profile.name(), env.name()))
	deploydir = path.join(path.dirname(path.dirname(bdir)), 'deploy', env.name())
	_dirs = (
		tmpdir,
		bdir,
		bdir + '.meta',
		deploydir,
	)
	for d in _dirs:
		if path.isdir(d):
			rmtree(d)
	_files = (
		bdir + '.zip',
		bdir + '.env',
		bdir + '.env.asc',
		bdir + '.deploy',
		bdir + '.lock',
		path.join(pdir, '.lock'),
	)
	for f in _files:
		if path.isfile(f):
			unlink(f)
	if mkdirs:
		for d in _dirs:
			makedirs(d)
	else:
		makedirs(tmpdir)

#
# testing plugins
#

from _sadm.utils import systemd
systemd._ctlcmd = ['systemctl']

from _sadmtest.plugin import Plugin

@pytest.fixture
def testing_plugin():
	return _newPlugin

def _newPlugin(name = 'testing', ns = '_sadm', cfgfn = None, deploy = False,
	buildDeploy = True, buildCfg = 'build.ini', cfgdir = 'config'):
	pdir = name.replace('.', path.sep)
	profile = 'plugin'
	config = None
	if deploy:
		profile = 'deploy'
		config = cfg.new(cfgfile = path.join('tdata', 'deploy.cfg'))
	env = _newEnv(profile = profile, name = name, config = config)
	if cfgfn is not None:
		env._cfgfile = path.join(pdir, cfgdir, cfgfn)
	p = Plugin(name, env, ns = ns)
	if deploy and buildDeploy:
		_buildDeploy(name, ns = ns, cfgfn = buildCfg)
	return p

def _buildDeploy(pname, ns = '_sadm', cfgfn = None):
	if cfgfn is None:
		cfgfn = 'build.ini'
	print('-- deploy plugin build:', pname)
	depdir = path.join('tdata', 'deploy', 'plugin', pname)
	targetdir = path.join('tdata', 'deploy.target', 'plugin', pname)
	for dirrm in (depdir, targetdir):
		if path.isdir(dirrm):
			rmtree(dirrm)
	p = _newPlugin(pname, ns = ns, cfgfn = cfgfn)
	p.build()
	makedirs(depdir, exist_ok = True)
	metadir = path.join('tdata', 'build', 'plugin', pname + '.meta')
	for fn in ('configure.ini', 'meta.json', pname + '.tar'):
		src = path.join(metadir, fn)
		dst = path.join(depdir, fn)
		move(src, dst)

#
# testing commands
#

import _sadm.cmd.deploy.deploy

from _sadmtest.cmd import TestingCmd

@pytest.fixture
def testing_cmd():
	def wrapper(cfgfile = 'deploy.cfg', env = 'testing', profile = 'cmd',
		config = 'config.ini', deploy = False):
		try:
			cfgfile = path.join('tdata', 'cmd', cfgfile)
			_sadm.deploy.cfgfile = cfgfile
			_sadm.cmd.deploy.deploy.cfgfile = cfgfile
			config = path.join('tdata', 'cmd', env or 'testing', config)
			if env is not None:
				_buildCmd(env, profile, config, deploy)
			return TestingCmd(config)
		finally:
			_sadm.deploy.cfgfile = path.join('tdata', 'cmd', 'deploy.cfg')
	return wrapper

def _buildCmd(env, profile, config, deploy):
	e = _newEnv(env, profile, action = 'build')
	e._cfgfile = config
	if deploy:
		ddir = path.join('tdata', 'deploy', profile, env)
		tdir = path.join('tdata', 'deploy.target', profile, env)
		for dirrm in (ddir, tdir):
			if path.isdir(dirrm):
				rmtree(dirrm)
		makedirs(ddir, exist_ok = True)
		mdir = path.join('tdata', 'build', profile, env + '.meta')
		for fn in ('configure.ini', 'meta.json', env + '.tar'):
			src = path.join(mdir, fn)
			dst = path.join(ddir, fn)
			move(src, dst)

#
# testing webapps
#

from _sadmtest.listen.wapp import ListenWebapp

@pytest.fixture
def listen_wapp():
	def wrapper(profile = ''):
		return ListenWebapp(profile)
	return wrapper

from _sadmtest.web.app import WebApp

@pytest.fixture
def testing_webapp():
	def wrapper(profile = ''):
		return WebApp(profile)
	return wrapper

from _sadmtest.devops.wapp import DevopsWebapp

@pytest.fixture
def devops_wapp():
	def wrapper(profile = ''):
		if profile != '':
			profile = '/'.join(['wapp', profile])
		return DevopsWebapp(profile)
	return wrapper
