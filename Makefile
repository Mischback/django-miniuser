# This Makefile is used as an interface to tox
#
# Still relying on make for convenience, because it offers tab completion for
# some common development tasks.
#
# Just type make to see the help on the available commands

APP := miniuser

.SILENT:
.PHONY: admin benchmark check clean compilemessages coverage createsuperuser \
		default diffsettings doc doc-srv flake8 help help-all isort isort-full \
		makemessages makemigrations migrate runserver shell test test-tag

# default target prints help
default: help

# django-admin.py version
# 	used to pass generic admin commands
admin_cmd ?= version
admin:
	tox -e django -- $(admin_cmd)

# counts LoC
benchmark:
	tox -e flake8 -- --benchmark

# django-admin.py check
check:
	$(MAKE) admin admin_cmd=check

# deletes all temporary files created by Django
clean:
	-tox -e coverage-report -- coverage erase
	find . -iname "*.pyc" -delete
	find . -iname "__pycache__" -delete
	find . -iname "test.sqlite" -delete
	find . -iname ".coverage.*" -delete
	rm -rf htmlcov

# django-admin.py compilemessages
compilemessages:
	$(MAKE) admin admin_cmd=compilemessages

# performs the tests and measures code coverage
coverage:   clean test
	tox -e coverage-report

# django-admin.py createsuperuser
createsuperuser: migrate
	$(MAKE) admin admin_cmd=createsuperuser

# django-admin.py diffsettings
diffsettings:
	$(MAKE) admin admin_cmd=diffsettings

# build the documentation using Sphinx
doc:
	tox -e doc

# access the documentation
doc-srv:
	tox -e doc-srv

# runs flake8 to check for PEP8 compliance
flake8:
	tox -e flake8

# TODO: document, how the "default" env can be changed in tox.ini [util]
help:
	echo "General commands"
	echo "  benchmark   Shows some statistics like LOC"
	echo "  clean       Cleans the environment"
	echo "  coverage    Reports code coverage for the test suite"
	echo "  doc         Builds the documenation using Sphinx"
	echo "  doc-srv     Serves the html documenation on port 8082"
	echo "  flake8      Checks source code for PEP8 compliance; additionally identifies"
	echo "                misaligned import statements"
	echo "  isort       Shows the proposed changes for Python imports using 'isort'"
	echo "  isort-full  Automatically sort Python imports in all source code files"
	echo "  test        Runs the test suite"
	echo "  test-tag    Runs the tests for a given tag (default: 'current')"
	echo "  tox              Runs tox"
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
	echo "  migrate          Actually applies the migrations into the common environment"
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
	echo "  doc              cd docs && make html"
	echo "  doc-srv          cd docs/build/html && python -m http.server 8082"
	echo "  flake8           flake8 ."
	echo "  isort            isort . --recursive --diff"
	echo "  isort-full       isort . --recursive"
	echo "  test             coverage run --parallel tests/runtests.py"
	echo "  test-tag         coverage run --parallel tests/runtests.py --tag=[current]"
	echo "  tox              tox"
	echo ""
	echo "  admin            django-admin.py [version]"
	echo "  check            django-admin.py check"
	echo "  compilemessages  django-admin.py compilemessages"
	echo "  diffsettings     django-admin.py diffsettings"
	echo "  makemessages     django-admin.py makemessages"
	echo "  makemigrations   django-admin.py makemigrations"
	echo "  migrate          django-admin.py migrate -v 0"
	echo "  runserver        django-admin.py runserver [0:8080]"
	echo "  shell            django-admin.py shell"
	echo ""
	echo "These commands are run in the [util] environment. If you want to specify a"
	echo "  different Python- or Django-version, change the settings in tox.ini [testenv:util]"
	echo ""

# only checking the imports and showing the diff
isort:
	tox -e isort -- --diff

# actually executes isort and changes the files!
isort-full:
	tox -e isort

# django-admin.py makemessages
makemessages:
	$(MAKE) admin admin_cmd="makemessages -a"

# django-admin.py makemigrations
makemigrations:
	$(MAKE) admin admin_cmd="makemigrations $(APP)"

# apply the migrations into the default environment
migrate:
	$(MAKE) admin admin_cmd="migrate -v 0"

# django-admin.py runserver 0:8080
host_port ?= 0:8080
runserver: migrate
	$(MAKE) admin admin_cmd="runserver $(host_port)"

# django-admin.py shell
shell_cmd ?= --version
shell:
	$(MAKE) admin admin_cmd="shell $(shell_cmd)"

# runs the tests in one single tox environment
test:
	tox -e test

# runs the tests with a given tag
tag ?= current
test-tag:
	tox -e test -- --tag=$(tag)

# find TODOs
todo_alt ?= TODO
todo_flags !=
todo:
	grep --color --exclude=.coverage --exclude-dir=.tox --exclude-dir=build -rnw$(todo_flags) . -e $(todo_alt)

tox:
#	tox | sed -f sed.todo | sed -e 'N;s/\(.*\) create: .*\nERROR: .*/Skipped \1/' | sed -e 'N;s/\(.*\) create: .*\nERROR: .*/Skipped \1/'
	tox
