#! /usr/bin/env bash
set -euo pipefail

pipenv run uvicorn \
    --host "0.0.0.0" \
    # --port $DATA_SERVER_PORT \
    app.main:app