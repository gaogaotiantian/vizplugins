refresh: clean build install lint

build:
	python setup.py build

install: 
	python setup.py install

build_dist:
	make clean
	python setup.py sdist bdist_wheel
	pip install dist/*.whl
	make test

release:
	python -m twine upload dist/*

lint:
	flake8 src tests --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 src tests --exclude tests/data/ --count --exit-zero --statistic --ignore=E501,E122,E126,E127,E128,W503

test:
	python -m unittest

coverage:
	env COVERAGE_RUN=True coverage run --parallel-mode --concurrency=multiprocessing -m unittest && coverage combine
	coverage report -m -i --include=*/vizplugins/*.py --omit=*tests*,*viztracer*,*psutil*

clean:
	rm -rf __pycache__
	rm -rf tests/__pycache__
	rm -rf src/vizplugins/__pycache__
	rm -rf build
	rm -rf dist
	rm -rf vizplugins.egg-info 
	rm -rf src/vizplugins.egg-info
	pip uninstall -y vizplugins 
