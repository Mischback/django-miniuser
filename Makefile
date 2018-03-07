APP := miniuser

LOCALPATH := ./
PYTHONPATH := $(LOCALPATH)/
PYTHON_BIN := $(VIRTUAL_ENV)/bin

TOX_UTIL_ENV := tox -e util
DJANGO_CMD := $(TOX_UTIL_ENV) -- django-admin.py
DJANGO_DEV_SETTINGS := tests.utils.settings_dev
DJANGO_DEV_POSTFIX := --settings=$(DJANGO_DEV_SETTINGS) --pythonpath=$(PYTHONPATH)

.SILENT:
.PHONY: admin benchmark check clean compilemessages coverage diffsettings \
		ensure_virtual_env flake8 help help-all isort isort-full makemessages \
		makemigrations runserver shell test test-tag


# django-admin.py version
# 	used to pass generic admin commands
admin_cmd ?= version
admin: ensure_virtual_env
	$(DJANGO_CMD) $(admin_cmd) $(DJANGO_DEV_POSTFIX)

benchmark: ensure_virtual_env
	tox -e flake8 -- --benchmark

# django-admin.py check
check: ensure_virtual_env
	$(DJANGO_CMD) check $(DJANGO_DEV_POSTFIX)

# deletes all temporary files created by Django
clean:
	find . -iname "*.pyc" -delete
	find . -iname "__pycache__" -delete
	find . -iname "test.sqlite" -delete
	find . -iname ".coverage.*" -delete
	$(TOX_UTIL_ENV) -- coverage erase
	rm -rf htmlcov

# django-admin.py compilemessages
compilemessages: ensure_virtual_env
	$(DJANGO_CMD) compilemessages $(DJANGO_DEV_POSTFIX)

# performs the tests and measures code coverage
coverage: ensure_virtual_env test
	tox -e coverage-report

# django-admin.py diffsettings
diffsettings: ensure_virtual_env
	$(DJANGO_CMD) diffsettings $(DJANGO_DEV_POSTFIX)

# most of the commands can only be used inside of the virtual environment
# TODO: get rid of this and install tox into systems Python
ensure_virtual_env:
	if [ -z $$VIRTUAL_ENV ]; then \
		echo "You don't have a virtualenv enabled."; \
		echo "Please enable the virtualenv first!"; \
		exit 1; \
	fi

# runs flake8 to check for PEP8 compliance
flake8: ensure_virtual_env
	tox -e flake8

# TODO: document, how the "default" env can be changed in tox.ini [util]
help:
	echo "General commands"
	echo "  benchmark   Shows some statistics like LOC"
	echo "  clean       Cleans the environment"
	echo "  coverage    Reports code coverage for the test suite"
	echo "  flake8      Checks source code for PEP8 compliance; additionally identifies"
	echo "                misaligned import statements"
	echo "  isort       Shows the proposed changes for Python imports using 'isort'"
	echo "  isort-full  Automatically sort Python imports in all source code files"
	echo "  test        Runs the test suite"
	echo "  test-tag    Runs the tests for a given tag (default: 'current')"
	echo ""
	echo "Django command shortcuts"
	echo "  admin            Generic wrapper to run django-admin CMD (default: 'version')"
	echo "                     Can be used like this 'make admin admin_cmd=\"shell\"' to"
	echo "                     run Django's shell."
	echo "  check            Runs the project's checks"
	echo "  compilemessages  Compiles the .po- to .mo-files"
	echo "  diffsettings     Shows the differences to Django's default settings"
	echo "  makemessages     Retrieves all strings marked for translation"
	echo "  makemigrations   Creates the migrations for the app"
	echo "  runserver        Runs Django's development server (default: 0:8080)"
	echo "                     You can specify a different host:port by setting host_port"
	echo "                     like 'make runserver host_port=0:7999'"
	echo "  shell            Runs Django's built-in shell"
	echo "                     By specifying shell_cmd a command can be run directly,"
	echo "                     'make shell shell_cmd=\"your command\"'"
	echo ""

help-tech:
	echo "Technical documentation"
	echo "  benchmark        flake8 . --benchmark"
	echo "  clean            [various find . -iname 'some file' -delete]"
	echo "  coverage         coverage run --parallel tests/runtests.py"
	echo "                   coverage combine"
	echo "                   coverage report"
	echo "  flake8           flake8 ."
	echo "  isort            isort . --recursive --diff"
	echo "  isort-full       isort . --recursive"
	echo "  test             coverage run --parallel tests/runtests.py"
	echo "  test-tag         coverage run --parallel tests/runtests.py --tag [current]"
	echo ""
	echo "  admin            django-admin.py [version]"
	echo "  check            django-admin.py check"
	echo "  compilemessages  django-admin.py compilemessages"
	echo "  diffsettings     django-admin.py diffsettings"
	echo "  makemessages     django-admin.py makemessages"
	echo "  runserver        django-admin.py runserver [0:8080]"
	echo "  shell            django-admin.py shell"
	echo ""

# only checking the imports and showing the diff
isort: ensure_virtual_env
	tox -e isort -- --diff

# actually executes isort and changes the files!
isort-full: ensure_virtual_env
	tox -e isort

# django-admin.py makemessages
makemessages: ensure_virtual_env
	$(DJANGO_CMD) makemessages -a $(DJANGO_DEV_POSTFIX)

# django-admin.py makemigrations
makemigrations: ensure_virtual_env
	$(DJANGO_CMD) makemigrations $(APP) $(DJANGO_DEV_POSTFIX)

# django-admin.py runserver 0:8080
host_port ?= 0:8080
runserver: ensure_virtual_env
	$(DJANGO_CMD) migrate -v 0 $(DJANGO_DEV_POSTFIX)
	$(DJANGO_CMD) runserver $(host_port) $(DJANGO_DEV_POSTFIX)

# django-admin.py shell
shell_cmd ?=
shell: ensure_virtual_env
	$(DJANGO_CMD) shell $(shell_cmd) $(DJANGO_DEV_POSTFIX)

# runs the tests in one single tox environment
test: ensure_virtual_env
	tox -e test

# runs the tests with a given tag
tag ?= current
test-tag: ensure_virtual_env
	tox -e test -- --tag $(tag)

tox: ensure_virtual_env
#	tox | sed -f sed.todo | sed -e 'N;s/\(.*\) create: .*\nERROR: .*/Skipped \1/' | sed -e 'N;s/\(.*\) create: .*\nERROR: .*/Skipped \1/'
	tox
