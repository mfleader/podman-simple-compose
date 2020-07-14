#! /usr/bin/env bash

# let the db start
# python /app/app/backend_pre_start.py

# generate migrations from schemas in app/db/base.py
alembic revision --autogenerate

# run migrations
alembic upgrade head

# seed db with user and superuser
python /app/app/initial_data.py