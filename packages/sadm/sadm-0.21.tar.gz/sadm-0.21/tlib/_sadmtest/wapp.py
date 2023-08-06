# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import bottle
import json

from io import BytesIO
from os import path

class TestingWebapp(object):
	profile = ''
	name = None
	cfgfn = None
	response = None
	_req = None

	def __init__(self, profile):
		if profile == '':
			self.profile = '.'
		else:
			self.profile = path.join(*profile.split('/'))
		fn = path.join('tdata', "%s.cfg" % self.name)
		if self.profile != '.':
			fn = path.join('tdata', self.name, self.profile, "%s.cfg" % self.name)
		self.cfgfn = fn

	def __postData(self, name):
		fn = path.join('tdata', self.name, self.profile, "%s.json" % name)
		with open(fn, 'r') as fh:
			return json.load(fh)

	def POST(self, pdata, callback, *args):
		self.response = None
		post = self.__postData(pdata)
		data = json.dumps(post['data']).encode('utf-8')
		headers = json.dumps(post['headers'])
		try:
			self.request(body = data, headers = headers)
			resp = callback(*args)
			self.response = resp.strip()
		finally:
			del bottle.request
			bottle.request = bottle.LocalRequest()

	def request(self, body = None, headers = {}):
		if self._req:
			return self._req
		# TODO: set headers
		blen = '0'
		if body is not None:
			blen = str(len(body))
		bottle.request.environ['CONTENT_LENGTH'] = blen
		bottle.request.environ['wsgi.input'] = BytesIO()
		if blen != '0':
			bottle.request.environ['wsgi.input'].write(body)
			bottle.request.environ['wsgi.input'].seek(0, 0)
		self._req = bottle.request
		return self._req

	def checkException(self, exc, status, match):
		err = exc.value
		assert err.status_code == status, \
			"error status got: %d - expect: %d" % (err.status_code, status)
		try:
			m = err.body.index(match) >= 0
		except ValueError:
			m = False
		assert m, "error did not match - got: %s - expect: %s" % (err.body, match)

	def checkRedirect(self, exc, status, location):
		resp = exc.value
		assert isinstance(resp, bottle.HTTPResponse)
		assert resp.status_code == status, \
			"redirect status got: %d - expect: %d" % (resp.status_code, status)
		loc = resp.headers.get('location')
		loc = loc.replace('http://127.0.0.1', '', 1)
		assert loc == location, \
			"redirect location got: '%s' - expect: '%s'" % (loc, location)
