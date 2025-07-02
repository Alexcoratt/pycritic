VENV?=.venv
PYTHON?=$(VENV)/bin/python
PIP?=$(VENV)/bin/pip


upload: setup
	$(PYTHON) -m twine upload dist/*

setup: setup_requirements
	$(PYTHON) setup.py sdist bdist_wheel

clean:
	rm -rf sdist bdist_wheel *.egg-info

%requirements:
	$(PIP) install --no-cache-dir -r $@.txt
