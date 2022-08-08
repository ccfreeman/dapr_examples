#!/bin/bash
set -e  # exit for nonzero codes (ie. nginx -t fails)

dapr run --app-id invoke-receiver --app-protocol grpc --app-port 50051 --config src/services/config.yaml -- pipenv run python -m src.services.server
