# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from collections import namedtuple, deque

from _sadm.devops.wapp import cfg
from _sadm.devops.wapp.tpl import tpl

__all__ = ['handle']

RepoList = namedtuple('RepoList', ('list',))
Repo = namedtuple('Repo', ('name', 'cfg'))

def handle(user):
	return tpl.parse('index', user = user, repos = _repos())

def _repos():
	config = cfg.config
	l = RepoList(deque())
	if config.has_section('devops.repo'):
		for name in config.options('devops.repo'):
			ena = config.getboolean('devops.repo', name, fallback = False)
			if ena:
				l.list.append(_getRepo(config, name))
	return l

def _getRepo(config, name):
	s = "devops.repo:%s" % name
	if config.has_section(s):
		return Repo(name, config[s])
	return None
