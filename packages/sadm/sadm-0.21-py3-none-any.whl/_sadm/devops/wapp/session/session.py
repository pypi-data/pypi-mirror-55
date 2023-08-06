# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from datetime import datetime
from secrets import token_urlsafe, token_hex
from typing import NamedTuple

from _sadm import log
from _sadm.devops.wapp import cfg
from _sadm.devops.wapp.session.db import SessionDB

__all__ = ['Session', 'WebappSession', 'init', 'check', 'new']

_secret = None
_tokenSize = 64

class Session(NamedTuple):
	pk: int
	id: str
	user: str
	last: datetime

class WebappSession(object):
	name = 'sadm_devops_session'
	_id = None

	def __init__(self):
		self._db = SessionDB(cfg.config)

	def cookie(self, req):
		log.debug('get cookie')
		if _secret is None:
			raise RuntimeError('session module not initialized')
		self._id = req.get_cookie(self.name, secret = _secret)
		return self._id

	def check(self, req):
		log.debug('check')
		self.cookie(req)
		if self._id is not None:
			row = self._db.get(self._id, update = True)
			if row:
				return Session(row['pk'], row['id'], row['user'], row['last'])
		return None

	def save(self, sessid, username):
		log.debug("save sid:%s user:%s" % (sessid, username))
		self._id = sessid
		ts = datetime.now()
		pk = self._db.save(self._id, username, ts)
		return Session(pk, self._id, username, ts)

def init(config):
	global _secret
	log.debug('init')
	_secret = token_urlsafe(_tokenSize)
	db = SessionDB(config)
	db.create()

def cookie(req):
	return WebappSession().cookie(req)

def new(resp, sid = None):
	if _secret is None:
		raise RuntimeError('session module not initialized')
	s = WebappSession()
	if sid is None: # pragma: no cover
		sid = token_hex(_tokenSize)
	resp.set_cookie(s.name, sid, secret = _secret, path = '/', httponly = True)
