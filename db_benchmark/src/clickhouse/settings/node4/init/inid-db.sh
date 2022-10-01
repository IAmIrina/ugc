#!/bin/bash

set -e
sleep 5
clickhouse client -n <<-EOSQL
	CREATE DATABASE IF NOT EXISTS replica;
	CREATE TABLE IF NOT EXISTS replica.metrics (event_time DateTime, user_id UUID, movie_id String, viewed_frame Int64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/metrics', 'replica_2') PARTITION BY toYYYYMMDD(event_time) ORDER BY (user_id, movie_id);
EOSQL


