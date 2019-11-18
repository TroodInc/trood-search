default: run

install:
	@pipenv install

run:
	@pipenv run python setup.py install
	@pipenv run python search/server.py

test:
	@pipenv run python setup.py install
	@pipenv run pytest -x

.PHONY: default run test
