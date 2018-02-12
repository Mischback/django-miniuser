APP := miniuser

LOCALPATH := ./
PYTHONPATH := $(LOCALPATH)/
PYTHON_BIN := $(VIRTUAL_ENV)/bin

DJANGO_TEST_SETTINGS := miniuser.tests.utils.project.settings
DJANGO_TEST_POSTFIX := --settings=$(DJANGO_TEST_SETTINGS) --pythonpath=$(PYTHONPATH)


.PHONY: all clean coverage ensure_virtual_env flake8 flake lint \
		test


all:
	@echo "Hello $(LOGNAME)! Welcome to django-app-skeleton"
	@echo ""
	@echo "  clean     Removes all temporary files"
	@echo "  coverage  Runs the tests and shows code coverage"
	@echo "  flake8    Runs flake8 to check for PEP8 compliance"
	@echo "              = flake / lint"
	@echo "  test      Runs the tests"


# performs the tests and measures code coverage
coverage: ensure_virtual_env test
	$(PYTHON_BIN)/coverage html
	$(PYTHON_BIN)/coverage report


# deletes all temporary files created by Django
clean:
	@find . -iname "*.pyc" -delete
	@find . -iname "__pycache__" -delete
	@rm -rf .coverage coverage_html


# most of the commands can only be used inside of the virtual environment
ensure_virtual_env:
	@if [ -z $$VIRTUAL_ENV ]; then \
		echo "You don't have a virtualenv enabled."; \
		echo "Please enable the virtualenv first!"; \
		exit 1; \
	fi


# runs flake8 to check for PEP8 compliance
flake8: ensure_virtual_env
	$(PYTHON_BIN)/flake8 .

flake: flake8

lint: flake8


# runs the tests
#	While we just have a bare project layout, this is more or less a dummy.
test: ensure_virtual_env
	@$(PYTHON_BIN)/coverage run $(PYTHON_BIN)/django-admin.py test $(APP) $(DJANGO_TEST_POSTFIX)
