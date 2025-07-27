.DEFAULT_GOAL := help
DC = docker compose
A = alembic

# BASE DOCKER COMMANDS
up: ## Build and start all services except certbot in detached mode.
	docker compose up --build -d --no-deps $(shell docker compose config --services)

down: ## Stop and remove all running services.
	${DC} down

restart: ## Restart all running services to apply any changes.
	${DC} restart

build: ## Rebuild all services, ensuring the latest changes are included.
	${DC} build

full-build: ## Build all services without using the cache, ensuring a fresh build.
	${DC} build --no-cache

logs: ## Display logs for all services, useful for monitoring and debugging.
	${DC} logs --follow

downgrade: ## Revert the database to the previous migration version using Alembic.
	${A} downgrade base

autogenerate: ## Generate a new migration script based on the current state of the models.
	${A} revision --autogenerate -m "First models migration"

upgrade: ## Apply all available database migrations to bring the schema up to date.
	${A} upgrade head

format: ## Formats the project code according to Black style rules to ensure code consistency.
	uvx black .

# HELP
.PHONY: help
help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@awk 'BEGIN {FS = ":.*?## "; section=""; prev_section=""} \
		/^[#].*/ { \
			section = substr($$0, 3); \
		} \
		/^[a-zA-Z0-9_-]+:.*?## / { \
			if (section != prev_section) { \
				print ""; \
				print "\033[1;34m" section "\033[0m"; \
				prev_section = section; \
			} \
			gsub(/\\n/, "\n                      \t\t"); \
			printf " \x1b[36;1m%-28s\033[0m%s\n", $$1, $$2; \
		}' $(MAKEFILE_LIST)
