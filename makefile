.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

run-prod: ## Run containers optimzed for the available hardware.
	docker compose up

run-dev: ## Run containers in development mode (code reloading + volume mounted as in local workspace)
	docker-compose -f docker-compose-dev.yml up

test: ## Run mypy & pytests. Spin up all the containers firsts as tests rely on redis cache.
	mypy */*.py
	docker-compose exec web pytest

rebuild: ## Rebuild all containers
	docker-compose build --force-rm --no-cache

ip: ## Show local ip addresses of the containers. Useful for configuring redis insights.
	@printf "Relay container local network ip: "
	@docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' relay
	
	@printf "Redis server container local network ip: "
	@docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' redis
	
	@printf "Redis insight container local network  ip: "
	@docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' redis-insight	

