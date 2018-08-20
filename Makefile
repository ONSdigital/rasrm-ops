build:
	pipenv install --dev

lint:
	pipenv run flake8 ./response_operations_ui ./tests
	pipenv check ./response_operations_ui ./tests

test: lint
	pipenv run pytest

start:
	pipenv run python run.py

docker: test
	docker build -t sdcplatform/rasrm-ops:latest .

docker-run: docker
	docker run --network=rasrmdockerdev_default  -p 8003:8003 sdcplatform/rasrm-ops:latest
