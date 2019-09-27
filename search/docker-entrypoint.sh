#!/bin/bash
set -e

echo "FIXME: should works without this step"
pipenv run python setup.py install

echo "Run server"
pipenv run python ./search/server.py
