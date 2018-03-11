Quickstart
==========

Use **django-miniuser** in your project
---------------------------------------

*coming really soon...*


Getting started with development
--------------------------------

**django-miniuser** completely relies on ``tox`` for testing and development.

If you cloned the repository, you'll find a ``tox.ini`` and a ``Makefile``. All
relevant settings are made in ``tox.ini``, so you will want to have a look into
that file first.

tox.ini
^^^^^^^

**django-miniuser** will runs its test agains several Python- and Django-versions.
Furthermore, code style (PEP8) will be checked aswell as the actual code coverage,
simply by running ``tox`` from command line.

If you want to have a deeper look, see the ``[testenv:util]``. This
environment is used to perform the most common tasks, like linting (using *flake8*
with an *isort*-plugin), running tests while developing (using your systems
default *python3*-version) and measuring code coverage (with *coverage*).

With the current *tox*-configuration, the ``util``-environment can be reused for
all this tasks, so it will not be recreated for each step.

In order to compile the *documentation*, the ``doc``-environment is used. It
features Sphinx to actually build the docs.

*Please note*, that the ``util``-environment will not install the code, but
use the actual code from your source code directory (currently, this is also
true for all test environments, but this will be changed as soon as possible).

Makefile
^^^^^^^^

The *Makefile* is just a convenient way of doing common development tasks. I
still like to rely on it, because ``make``'s targets allow tab completion with
*zsh* (and probably *bash* and other shells).

If you are interested in this, just type ``make`` on your (\*nix) shell and you
will be good to go (it will print the available commands).

Currently, the *Makefile* still relies on being executed/used inside of a
virtualenv. Since all commands are executed in *tox*-environemnts, this is not
really necessary and will be removed as soon as possible.
