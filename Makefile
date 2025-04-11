# Path to docker-compose files
COMPOSE := docker-compose \
  -f docker/docker-compose.base.yml \
  -f docker/docker-compose.postgres.yml \
  -f docker/docker-compose.redis.yml \
  -f docker/docker-compose.mongoDB.yml \
  -f docker/docker-compose.kafka.yml \
  -f docker/docker-compose.services.yml

# Basic
up:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down -v --remove-orphans

logs:
	$(COMPOSE) logs -f

restart:
	$(MAKE) down
	$(MAKE) up

ps:
	$(COMPOSE) ps

build:
	$(COMPOSE) build

rebuild:
	$(COMPOSE) down --remove-orphans
	$(COMPOSE) build
	$(COMPOSE) up

# recreating Zookeeper changes cluster.id ,
# you need to clear the Kafka volume, or write it manually, but that's lazy
rebuild-kafka:
	docker-compose \
		-f docker/docker-compose.base.yml \
		-f docker/docker-compose.kafka.yml \
		down -v --remove-orphans
	docker-compose \
		-f docker/docker-compose.base.yml \
		-f docker/docker-compose.kafka.yml \
		up -d --build

restart-services:
	docker-compose \
		-f docker/docker-compose.base.yml \
		-f docker/docker-compose.postgres.yml \
		-f docker/docker-compose.redis.yml \
		-f docker/docker-compose.mongoDB.yml \
		-f docker/docker-compose.kafka.yml \
		-f docker/docker-compose.services.yml \
		up -d --build

validate:
	$(COMPOSE) config


# for PowerShell
# $env:DOCKER_USER = "your_name"
# for bash
# export DOCKER_USER=your_name
DOCKER_USER ?= unknown


build-shortener:
	docker build -f backend/shortener_service/Dockerfile -t $(DOCKER_USER)/shortener-service:latest backend

push-shortener:
	docker push $(DOCKER_USER)/shortener-service:latest

build-validator:
	docker build -f backend/url-validator/Dockerfile -t $(DOCKER_USER)/url-validator:latest backend

push-validator:
	docker push $(DOCKER_USER)/url-validator:latest

build-all: build-shortener build-validator

push-all: push-shortener push-validator