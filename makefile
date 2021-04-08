install:
	pip install -e .['dev'] --ignore-installed

db:
	flask create-db 

uninstall: 
	pip uninstall camara
	rm -rf sys.db

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	rm -rf __pycache__
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build
	#pip install -e .['dev'] --upgrade --no-cache --ignore-installed
	
test:
	pytest tests -vv


