# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import os
import os.path
import sqlite3

from datetime import datetime

from _sadm import log
from _sadm.utils import sh, path

__all__ = ['SessionDB']

_detectTypes = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES

_sessTable = """
CREATE TABLE IF NOT EXISTS sess (
	pk INTEGER PRIMARY KEY AUTOINCREMENT,
	id VARCHAR(128) NOT NULL UNIQUE,
	user VARCHAR(1024) NOT NULL UNIQUE,
	last timestamp
);
"""
_sessGet = 'SELECT pk, id, user, last FROM sess WHERE id = ?;'
_sessLast = 'UPDATE sess SET last = ? WHERE id = ?;'
_sessNew = 'INSERT INTO sess (id, user, last) VALUES (?, ?, ?);'
_sessSave = 'UPDATE sess SET id = ?, last = ? WHERE user = ?;'
_sessUser = 'SELECT pk, id, user, last FROM sess WHERE user = ?;'

class SessionDB(object):
	_uri = None
	_mem = False
	_dir = None
	_fn = None

	def __init__(self, config):
		dbdir = config.get('devops', 'session.dbdir',
			fallback = path.join('~', '.local', 'sadm', 'devops', 'wapp'))
		if dbdir == ':memory:':
			self._uri = 'file:session.db?mode=memory&cache=shared'
			self._mem = True
		else:
			self._fn = os.path.abspath(path.join(dbdir, 'session.db'))
			self._uri = "file:%s?cache=shared" % self._fn
		self._dir = dbdir

	def _connect(self):
		log.debug("connect %s" % self._uri)
		conn = sqlite3.connect(self._uri, uri = True, detect_types = _detectTypes)
		conn.row_factory = sqlite3.Row
		return conn

	def create(self):
		log.debug("create db - mem:%s dir:%s" % (self._mem, self._dir))
		if self._mem:
			self._mkdb()
		else:
			if os.path.isdir(self._dir):
				log.debug("%s: db dir exists" % self._dir)
			else:
				log.debug("create db dir: %s" % self._dir)
				os.makedirs(self._dir)
			with sh.lockd(self._dir):
				self._mkdb()

	def _mkdb(self):
		with self._connect() as db:
			db.execute(_sessTable)
			db.commit()

	def get(self, sessid, update = False):
		row = None
		with self._connect() as db:
			cur = db.execute(_sessGet, (sessid,))
			row = cur.fetchone()
			if row and update:
				ts = datetime.now()
				db.execute(_sessLast, (ts, sessid))
				db.commit()
				row = dict(row)
				row['last'] = ts
		return row

	def _user(self, db, name):
		cur = db.execute(_sessUser, (name,))
		return cur.fetchone()

	def save(self, sessid, username, ts):
		pk = None
		with self._connect() as db:
			cur = None
			if self._user(db, username) is None:
				cur = db.execute(_sessNew, (sessid, username, ts))
			else:
				cur = db.execute(_sessSave, (sessid, ts, username))
			db.commit()
			pk = cur.lastrowid
		if pk is None:
			r = self.get(sessid)
			pk = r['pk']
		return pk
