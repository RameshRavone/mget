PYTHON = python3

build:
	$(PYTHON) setup.py build

install:
	$(PYTHON) setup.py install

clean:
	$(PYTHON) setup.py clean
	rm -r build/ dist/ mget.egg-info/

dist:
	$(PYTHON) setup.py sdist

upload:
	$(PYTHON) setup.py sdist upload
