## Start Kafka

    cd composes/kafka

    docker-compose up -d

## Start Postgres

    cd composes/postgreSQL

    docker-compose up -d

## Run worker

- set env variables
  - source dev_env.sh
- run worker
  - python kafka_worker.py

## Install lib

pip install psycopg2-binary
