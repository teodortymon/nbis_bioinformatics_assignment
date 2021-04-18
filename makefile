.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

run-prod: ## Run containers with worker count optimized to available CPU (by default 1x the amount of cores)
	docker compose up

run-dev: ## Run containers in development mode with code reloading and /app volume mounted in local workspace for active development
	docker compose -f docker-compose-dev.yml up

test: ## Run mypy & pytests. Spin up all the containers in dev mode firsts as integration tests rely on redis cache and local test files
	docker compose exec web pytest
	docker compose exec web mypy */*.py

shell: ## Atttach a bash shell to the relay container
	docker exec -it relay /bin/bash

rebuild: ## Rebuild all containers
	docker compose build --force-rm --no-cache

ip: ## Show local ip addresses of the containers. Useful for configuring redis insights.
	@printf "Relay container local network ip: "
	@docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' relay
	
	@printf "Redis server container local network ip: "
	@docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' redis
	
	@printf "Redis insight container local network  ip: "
	@docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' redis-insight	

