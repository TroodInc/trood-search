default: all

all: build run

build:
	@echo Build project ...
	@docker-compose build

run:
	@docker-compose -f docker-compose.test.yml up -d
	@make wait-database
	@make init-custodian
	@make init-sphinx
	@make ps

wait-database:
	@echo wait database ...
	@for i in 1 2 3; do sleep 5; done;

init-custodian:
	@echo Init custodian database
	@docker-compose -f docker-compose.test.yml exec -T custodian sh -c 'rm -rf /home/custodian/*'
	@docker-compose -f docker-compose.test.yml exec -T postgres psql -U postgres -d custodian -c "drop schema public cascade; create schema public;"
	@docker-compose -f docker-compose.test.yml restart custodian
	@docker-compose -f docker-compose.test.yml exec -T custodian python /usr/bin/migrate.py

init-sphinx:
	@echo Init sphinx search index
	@docker-compose -f docker-compose.test.yml exec -T sphinxsearch sh -c 'rm -rf /var/lib/sphinxsearch/data/*'

ps:
	@docker-compose -f docker-compose.test.yml ps

down:
	@docker-compose -f docker-compose.test.yml down

restart: down run
