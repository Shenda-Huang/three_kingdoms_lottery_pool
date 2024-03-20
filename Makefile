# -*- makefile -*-

PYTHON_VERSION?=3.11
PYTHON_BIN:=python$(PYTHON_VERSION)
PYTHON_SYSTEM_BIN:=$(shell which $(PYTHON_BIN))

define PYTHON_RUN
	@( $(if $(VIRTUAL_ENV),python, $(if $(container),$(PYTHON_SYSTEM_BIN),source $(VENV_DIR)/bin/activate && python) ) $(1) )
endef

PYTHON_FILES:=$(shell find * -iname '*.py' -type f)

VENV_DIR:=.venv

.PHONY: all
all: help

.PHONY: help
help: ## Show this help message.
	@echo 'usage: make [target] ...' && \
	echo && \
	echo 'targets:' && \
	perl -ne '/^(.*)\:(.*)##\ (.*)$$/ && print "$$1#$$3\n";' $(MAKEFILE_LIST) | column -t -c 2 -s '#'

.PHONY: install-requirements
install-requirements:
	(source $(VENV_DIR)/bin/activate && python -m pip install -r requirements-dev.txt) 2>&1 | tee $@.log

$(VENV_DIR):
	$(PYTHON_SYSTEM_BIN) -m venv $(VENV_DIR)
	$(MAKE) install-requirements

.PHONY: venv
venv: $(VENV_DIR) ## Create venv

.PHONY: clean
clean: ## Clean build artifacts
	-rm -rf .mypy_cache/
	-rm -rf dist/
	-rm -rf build_output/
	-rm -rf *.egg-info
	-rm -f *.log*
	-rm -rf temp/

.PHONY: realclean
realclean: clean ## Clean build artifacts and delete virtual env
	-rm -rf $(VENV_DIR)/
	-rm -rf dist/
	-find * -iname "*.pyc" -type f | xargs rm -f
	-find * -iname "__pycache__" -type d | xargs rm -rf
	-find * -iname "*.egg-info" -type d | xargs rm -rf

.PHONY: black
black: ## Format python code using black
	$(call PYTHON_RUN, -m black $(PYTHON_FILES))

.PHONY: pylint
pylint: ## Run pylint for python code
	$(call PYTHON_RUN, -m pylint $(PYTHON_FILES))

.PHONY: mypy
mypy: ## Run mypy for python code
	$(call PYTHON_RUN, -m mypy $(PYTHON_FILES))

.PHONY: pytest
pytest: ##  Run pytest
	$(call PYTHON_RUN, -m pytest -v)

.PHONY: run-lottery
run-lottery: ##  Run from source
	$(call PYTHON_RUN, ./run-lottery.py --log-level DEBUG run-lottery)

# vim:ft=make