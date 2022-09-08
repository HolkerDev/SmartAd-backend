test:
	python -m unittest discover src/tests/ -v
deploy:
	sls deploy --aws-profile private
update:
	pip install -t src/vendor -r requirements.txt