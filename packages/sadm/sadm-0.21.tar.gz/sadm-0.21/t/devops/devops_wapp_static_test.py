# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from bottle import HTTPError, HTTPResponse

from _sadm.devops.wapp.static import static

def test_serve_refuse():
	err = static.serve('testing.txt')
	assert isinstance(err, HTTPError)
	assert err.status_code == 404

def test_serve_notfound():
	err = static.serve('notfound.css')
	assert isinstance(err, HTTPError)
	assert err.status_code == 404

def test_default_css():
	err = static.serve('default.css')
	assert isinstance(err, HTTPResponse)
	assert err.status_code == 200
