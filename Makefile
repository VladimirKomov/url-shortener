# Path to docker-compose files
COMPOSE := docker-compose \
  -f docker/docker-compose.base.yml \
  -f docker/docker-compose.postgres.yml \
  -f docker/docker-compose.redis.yml \
  -f docker/docker-compose.mongoDB.yml \
  -f docker/docker-compose.kafka.yml \
  -f docker/docker-compose.services.yml

# Basic команды
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

validate:
	$(COMPOSE) config
