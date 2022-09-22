#!/bin/bash
set -e

clickhouse client -n <<-EOSQL
	CREATE DATABASE  IF NOT EXISTS default;
	CREATE TABLE  IF NOT EXISTS default.metrics (event_time DateTime, user_id UUID, movie_id String, viewed_frame Int64) ENGINE = MergeTree();
    TRUNCATE TABLE default.metrics
EOSQL

clickhouse-client --format_csv_delimiter="," --query="INSERT INTO metrics FORMAT CSV" < /etc/benchmark_data/frames.csv

