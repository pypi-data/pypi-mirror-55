#!/bin/sh
rm -rfv build dist .pytest_cache
rm -rfv tdata/build tdata/tmp tdata/deploy tdata/deploy.target
rm -rfv htmlcov .coverage .coverage.* coverage.xml
rm -rfv docs/_build docs/doctrees
find . -type d -name __pycache__ | xargs rm -rfv
