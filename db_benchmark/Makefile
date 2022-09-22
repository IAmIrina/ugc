burn:
	python3 src/data_generator.py
	docker-compose -f docker-compose.yml  up --build
vertica:
	python3 src/data_generator.py
	docker-compose -f docker-compose-vertica.yml  up --build
clickhouse:
	python3 src/data_generator.py
	docker-compose -f docker-compose-clickhouse.yml  up --build
clickhouse-cluster:
	python3 src/data_generator.py
	docker-compose -f docker-compose-clickhouse-cluster.yml  up --build