#! /usr/bin/env bash

# let the db start
python /app/app/backend_pre_start.py

# run migrations
alembic upgrade head

# create initial data in db
python /app/app/initial_data.py