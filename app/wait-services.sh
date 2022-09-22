#!/bin/sh

cmd="$@"

while ! nc -z -v $KAFKA_HOST $KAFKA_PORT;
do
  >&2 echo "Kafka is unavailable - sleeping"
  sleep 2;
done

exec $cmd