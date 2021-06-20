run:
	python main.py

test:
	pytest tests

docker-build:
	  docker build -t ml-web-server:1.0 .

docker-run:
	docker run -p 8000:8000  --name ML-web-server -d ml-web-server:1.0


docker-down:
	docker stop ML-web-server

docker-test:
	docker exec -t ML-web-server pytest tests