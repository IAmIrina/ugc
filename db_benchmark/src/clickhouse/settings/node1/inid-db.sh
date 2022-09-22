#!/bin/bash
set -e

clickhouse client -n <<-EOSQL
	CREATE DATABASE shard;
	CREATE DATABASE replica;
	CREATE TABLE shard.metrics (event_time DateTime, user_id UUID, movie_id String, viewed_frame Int64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/metrics', 'replica_1') PARTITION BY toYYYYMMDD(event_time) ORDER BY (user_id, movie_id);
	CREATE TABLE replica.metrics (event_time DateTime, user_id UUID, movie_id String, viewed_frame Int64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/metrics', 'replica_2') PARTITION BY toYYYYMMDD(event_time) ORDER BY (user_id, movie_id);
	CREATE TABLE default.metrics (event_time DateTime, user_id UUID, movie_id String, viewed_frame Int64) ENGINE = Distributed('company_cluster', '', metrics, rand());
	TRUNCATE TABLE default.metrics    
EOSQL

clickhouse-client --format_csv_delimiter="," --query="INSERT INTO default.metrics FORMAT CSV" < /etc/benchmark_data/frames.csv

