# Makefile to help automate tasks
WD := $(shell pwd)
PY := .venv/bin/python
PIP := .venv/bin/pip
PEP8 := .venv/bin/pep8
PYTEST := .venv/bin/py.test
FLAKE8 := .venv/bin/flake8


# #######
# INSTALL
# #######
.PHONY: all
all: sysdeps .venv

.PHONY: clean-all
clean-all: clean_venv
	if [ -d dist ]; then \
		rm -r dist; \
    fi


sysdeps:


.venv: .venv/bin/python
.venv/bin/python:
	virtualenv -p /usr/bin/python3 .venv
	$(PIP) install juju
	$(PIP) install click

.PHONY: clean_venv
clean_venv:
	rm -rf .venv


.venv/bin/flake8: .venv
	$(PIP) install flake8

lint: .venv/bin/flake8
	$(FLAKE8) stressjuju


###
# Stress Test Juju
###

