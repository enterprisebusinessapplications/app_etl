ENV_FILE?=.env
-include $(ENV_FILE)
build:
	docker compose --env-file $(ENV_FILE) -f docker-compose.build.yaml build app_etl