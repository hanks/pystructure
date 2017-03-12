.PHONY: cut-release build upload test clean

test:
	tox

cut-release:
	standard-version

build:
	rm -rf dist
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*

clean:
	rm -rf dist
	rm -rf pystructure.egg-info
