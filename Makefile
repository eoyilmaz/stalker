SHELL:=bash
PACKAGE_NAME=stalker
NUM_CPUS = $(shell nproc ||  grep -c '^processor' /proc/cpuinfo)
SETUP_PY_FLAGS = --use-distutils
VERSION := $(shell cat VERSION)
VERSION_FILE=$(CURDIR)/VERSION
VIRTUALENV_DIR:=.venv
SYSTEM_PYTHON?=python3

all: build FORCE

.PHONY: help
help:
	@echo ""
	@echo "Available targets:"
	@make -qp | grep -o '^[a-z0-9-]\+' | sort

.PHONY: venv
venv:
	@printf "\n\033[36m--- $@: Creating Local virtualenv '$(VIRTUALENV_DIR)' using '$(SYSTEM_PYTHON)' ---\033[0m\n"
	$(SYSTEM_PYTHON) -m venv $(VIRTUALENV_DIR)

build:
	@printf "\n\033[36m--- $@: Building ---\033[0m\n"
	echo -e "\n\033[36m--- $@: Local install into virtualenv '$(VIRTUALENV_DIR)' ---\033[0m\n";
	source ./$(VIRTUALENV_DIR)/bin/activate; \
	echo -e "\n\033[36m--- $@: Using python interpretter '`which python`' ---\033[0m\n"; \
	pip install -r requirements.txt; \
	pip install -r requirements-dev.txt; \
	python -m build;

.PHONY: install
install:
	@printf "\n\033[36m--- $@: Installing $(PACKAGE_NAME) to virtualenv at '$(VIRTUALENV_DIR)' using '$(SYSTEM_PYTHON)' ---\033[0m\n"
	source ./$(VIRTUALENV_DIR)/bin/activate; \
	pip install ./dist/$(PACKAGE_NAME)-$(VERSION)-*.whl --force-reinstall;

clean: FORCE
	@printf "\n\033[36m--- $@: Clean ---\033[0m\n"
	-rm -rf .pytest_cache
	-rm -f .coverage.*
	-rm -rf dist
	-rm -rf build
	-rm -rf docs/build
	-rm -rf docs/source/generated/*

clean-all: clean
	@printf "\n\033[36m--- $@: Clean All---\033[0m\n"
	-rm -f INSTALLED_FILES
	-rm -f setuptools-*.egg
	-rm -f use-distutils
	-rm -f .coverage*
	-rm -Rf .tox
	-rm -Rf htmlcov
	-rm -rf dist
	-rm -Rf src/$(PACKAGE_NAME).egg-info
	-rm -Rf $(VIRTUALENV_DIR)

html:
	./setup.py readme

new-release:
	@printf "\n\033[36m--- $@: Generating New Release ---\033[0m\n"
	git add $(VERSION_FILE)
	git commit -m "Version $(VERSION)"
	git push
	git checkout main
	git pull
	git merge develop
	git tag $(VERSION)
	git push origin main --tags
	source ./$(VIRTUALENV_DIR)/bin/activate; \
	echo -e "\n\033[36m--- $@: Using python interpretter '`which python`' ---\033[0m\n"; \
	pip install -r requirements.txt; \
	pip install -r requirements-dev.txt; \
	python -m build; \
	twine check dist/$(PACKAGE_NAME)-$(VERSION).tar.gz; \
	twine upload dist/$(PACKAGE_NAME)-$(VERSION).tar.gz;

.PHONY: tests
tests:
	@printf "\n\033[36m--- $@: Run Tests ---\033[0m\n"
	echo -e "\n\033[36m--- $@: Using virtualenv at '$(VIRTUALENV_DIR)' ---\033[0m\n";
	source ./$(VIRTUALENV_DIR)/bin/activate; \
	echo -e "\n\033[36m--- $@: Using python interpretter '`which python`' ---\033[0m\n"; \
	PYTHONPATH=src pytest -n auto -W ignore --color=yes --cov=src --cov-report term --cov-report html --cov-fail-under 99 tests;

.PHONY: docs
docs:
	cd docs && $(MAKE) html

# https://www.gnu.org/software/make/manual/html_node/Force-Targets.html
FORCE:
