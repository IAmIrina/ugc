#!/bin/bash

set -e
sleep 5
clickhouse client -n <<-EOSQL
	CREATE DATABASE IF NOT EXISTS shard;
	CREATE TABLE IF NOT EXISTS shard.metrics (event_time DateTime, user_id UUID, movie_id String, viewed_frame Int64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/metrics', 'replica_1') PARTITION BY toYYYYMMDD(event_time) ORDER BY (user_id, movie_id);
	CREATE TABLE IF NOT EXISTS default.metrics (event_time DateTime, user_id UUID, movie_id String, viewed_frame Int64) ENGINE = Distributed('company_cluster', '', metrics, rand());   
EOSQL


