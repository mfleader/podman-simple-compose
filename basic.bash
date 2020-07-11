#! /bin/bash

podname=snappy
PGPASSWORD=secret
PGUSER=user
SECRET=secret
PGPORT=5432
pgvol=pgvol
DBNAME=postgres

# database uri
cxnstr=postgres+psycopg2://$PGUSER:$PGPASSWORD@localhost:$PGPORT/$DBNAME


podman pod exists $podname && podman pod rm $podname

podman create $pgvol

podman run \
    --detach \
    --env POSTGRES_PASSWORD=$PGPASSWORD \
    --env POSTGRESQL_USER=$PGUSER \
    --name db-svc \
    --pod $podname \
    --publish $PGPORT \
    --volume $pgvol \
    postgres:12.3-alpine
    
