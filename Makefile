help:
	@echo "usage: make <target>"
	@echo "Targets:"
	@echo "	up-ugc"
	@echo "	up-etl"
	@echo "	up-elk"


up-ugc:
	docker-compose -f docker-compose.dev.yml up  --build
up_elk:
	docker-compose -f docker-compose.dev.yml -f docker-compose.elk.yml up --build