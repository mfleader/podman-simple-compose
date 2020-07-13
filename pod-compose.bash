#! /bin/bash

source .env

podname=snappy
pgvol=pgvol


podman pod exists $podname && podman pod rm $podname

podman create $pgvol

podman run \
    --detach \
    --env POSTGRES_PASSWORD=$PGPASSWORD \
    --env POSTGRESQL_USER=$PGUSER \
    --name db-svc \
    --pod $podname \
    --publish $PGPORT \
    --volume $pgvol:/var/lib/postgresql/data \
    postgres:12.3-alpine
    

podman run \
    --detach
    --name api
    --pod $podname \
    localhost/users