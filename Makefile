APP := miniuser

LOCALPATH := ./
PYTHONPATH := $(LOCALPATH)/
PYTHON_BIN := $(VIRTUAL_ENV)/bin

DJANGO_DEV_SETTINGS := tests.utils.settings_dev
DJANGO_DEV_POSTFIX := --settings=$(DJANGO_DEV_SETTINGS) --pythonpath=$(PYTHONPATH)


.PHONY: all benchmark clean coverage ensure_virtual_env flake8 flake isort/diff isort \
		migrations test


# TODO: document all available commands
all:
	@echo ""
	@echo " Hello $(LOGNAME)! Welcome to django-$(APP)"
	@echo ""
	@echo "   clean      Removes all temporary files"
	@echo "   coverage   Runs the tests and shows code coverage"
	@echo "   flake8     Runs flake8 to check for PEP8 compliance (alias: flake)"
	@echo "   isort      Runs isort to actually modify the imports"
	@echo "   isort/diff Runs isort --diff to show proposed changes"
	@echo "   migrations Creates the migrations for the app $(APP)"
	@echo "   test       Runs the tests"
	@echo ""

benchmark: ensure_virtual_env
	@tox -e flake8 -- --benchmark

# deletes all temporary files created by Django
clean:
	@find . -iname "*.pyc" -delete
	@find . -iname "__pycache__" -delete
	@find . -iname "test.sqlite" -delete
	@find . -iname ".coverage.*" -delete
	@tox -e util -- coverage erase
	@rm -rf htmlcov

# performs the tests and measures code coverage
coverage: ensure_virtual_env test
	@tox -e coverage-report

# most of the commands can only be used inside of the virtual environment
ensure_virtual_env:
	@if [ -z $$VIRTUAL_ENV ]; then \
		echo "You don't have a virtualenv enabled."; \
		echo "Please enable the virtualenv first!"; \
		exit 1; \
	fi

# runs flake8 to check for PEP8 compliance
flake8: ensure_virtual_env
	@tox -e flake8

flake: flake8

# actually executes isort and changes the files!
isort: ensure_virtual_env
	@tox -e isort

# only checking the imports and showing the diff
isort/diff: ensure_virtual_env
	@tox -e isort -- --diff

# creates the necessary migrations
#	this should be done after any model changes
# TODO: make this run in tox's util environment!
migrations: ensure_virtual_env
	# @$(PYTHON_BIN)/django-admin.py makemigrations $(APP) $(DJANGO_DEV_POSTFIX)
	# @tox -e util -- django-admin.py makemigrations $(APP) $(DJANGO_DEV_POSTFIX)
	@echo "This is currently in development

# runs the tests in one single tox environment
test: ensure_virtual_env
	@tox -e util
