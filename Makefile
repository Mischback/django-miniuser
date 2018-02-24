APP := miniuser

LOCALPATH := ./
PYTHONPATH := $(LOCALPATH)/
PYTHON_BIN := $(VIRTUAL_ENV)/bin

DJANGO_DEV_SETTINGS := tests.utils.settings_dev
DJANGO_DEV_POSTFIX := --settings=$(DJANGO_DEV_SETTINGS) --pythonpath=$(PYTHONPATH)


.PHONY: all benchmark clean coverage ensure_virtual_env flake8 flake isort/diff isort \
		migrations test


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
	@$(PYTHON_BIN)/flake8 --benchmark .

# performs the tests and measures code coverage
coverage: ensure_virtual_env test
	@$(PYTHON_BIN)/coverage combine
	# $(PYTHON_BIN)/coverage html
	@$(PYTHON_BIN)/coverage report

# deletes all temporary files created by Django
clean:
	@find . -iname "*.pyc" -delete
	@find . -iname "__pycache__" -delete
	@find . -iname "test.sqlite" -delete
	@rm -rf .coverage .coverage_html

# most of the commands can only be used inside of the virtual environment
ensure_virtual_env:
	@if [ -z $$VIRTUAL_ENV ]; then \
		echo "You don't have a virtualenv enabled."; \
		echo "Please enable the virtualenv first!"; \
		exit 1; \
	fi

# runs flake8 to check for PEP8 compliance
flake8: ensure_virtual_env
	@$(PYTHON_BIN)/flake8 .

flake: flake8

# actually executes isort and changes the files!
isort: ensure_virtual_env
	@$(PYTHON_BIN)/isort --recursive .

# only checking the imports and showing the diff
isort/diff: ensure_virtual_env
	@$(PYTHON_BIN)/isort --diff --recursive .

# creates the necessary migrations
#	this should be done after any model changes
migrations: ensure_virtual_env
	@$(PYTHON_BIN)/django-admin.py makemigrations $(APP) $(DJANGO_DEV_POSTFIX)

test: ensure_virtual_env
	@$(PYTHON_BIN)/tox -e py35-django20
