COMPOSE=docker-compose \
  -f docker/docker-compose.base.yml \
  -f docker/docker-compose.postgres.yml \
  -f docker/docker-compose.redis.yml \
  -f docker/docker-compose.mongoDB.yml \
  -f docker/docker-compose.kafka.yml \
  -f docker/docker-compose.services.yml \

up:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down -v --remove-orphans

logs:
	$(COMPOSE) logs -f

restart:
	$(MAKE) down
	$(MAKE) up
