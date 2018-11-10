.EXPORT_ALL_VARIABLES:
PIPENV_VENV_IN_PROJECT = 1

all: .installed tests

install:
	@rm -f .installed  # force re-install
	@make .installed

.installed: Pipfile Pipfile.lock
	@echo "Pipfile(.lock) is newer than .installed, (re)installing"
	@pipenv install --dev
	@pipenv run pre-commit install -f --hook-type pre-commit
	@pipenv run pre-commit install -f --hook-type pre-push
	@echo "This file is used by 'make' for keeping track of last install time. If Pipfile or Pipfile.lock are newer then this file (.installed) then all 'make *' commands that depend on '.installed' know they need to run pipenv install first." \
		> .installed

# Run development server
run: .installed
	@pipenv run pserve etc/development.ini

# Testing and linting
lint: .installed
	@pipenv run pre-commit run --all-files --hook-stage push

type: types
types: .installed
	@# Delete .mypy_cache because mypy report is not generated when cache is fresh https://github.com/python/mypy/issues/5103
	@rm -rf .mypy_cache
	@pipenv run mypy run.py
	@cat ./typecov/linecount.txt
	@pipenv run python .travis/type_coverage_threshold.py 100 ./typecov/linecount.txt

sort: .installed
	@pipenv run isort -rc --atomic run.py
	@pipenv run isort -rc --atomic tests.py

fmt: format
black: format
format: .installed sort
	@pipenv run black --py36 run.py
	@pipenv run black --py36 tests.py
	@pipenv run black --py36 .travis/type_coverage_threshold.py

# anything, in regex-speak
filter = "."
# additional arguments for pytest
args = ""

unit: .installed
	@pipenv run pytest tests.py --cov-report html --cov-report xml:cov.xml --cov-report term-missing --cov-fail-under=100 --cov=run --cov-branch -k $(filter) $(args)

test: tests
tests: format lint types unit

clean:
	@if [ -d ".venv/" ]; then pipenv --rm; fi
	@rm -rf .coverage .mypy_cache htmlcov/ htmltypecov/ xunit.xml typecov \
	    .git/hooks/pre-commit .git/hooks/pre-push
	@rm -f .installed
