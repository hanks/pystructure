.PHONY: cut-release build release test clean

test:
	tox

cut-release:
	standard-version

build:
	rm -rf dist
	rm -rf pystructure.egg-info
	python setup.py sdist bdist_wheel

release:
	rm -rf dist
	rm -rf pystructure.egg-info
	python setup.py sdist bdist_wheel
	twine upload dist/*

clean:
	rm -rf dist
	rm -rf pystructure.egg-info
