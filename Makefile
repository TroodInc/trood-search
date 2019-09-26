default: all

all: build run

build:
	@echo Check docker-compose.yml
	@docker-compose config -q
	@echo Build project ...
	@docker-compose build

run:
	@docker-compose up -d
	@make wait-database
	@make create-search-index

wait-database:
	@echo wait database ...
	@for i in 1 2 3; do sleep 5; done;

create-search-index:
	@echo Creating sphinx search index ...
	@docker-compose restart sphinxsearch

down:
	@docker-compose down

restart: down run
