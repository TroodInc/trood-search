default: run

install:
	@pipenv install

run:
	@pipenv run uvicorn search.main:app --reload

test:
	@pipenv run pytest -x

black:
	@pipenv run black -l 79 .

isort:
	@pipenv run isort ${file}

.PHONY: default run test
