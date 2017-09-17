#!/usr/bin/env bash

docker build -t fischerfredl/bp-geo:latest .
docker push fischerfredl/bp-geo:latest
docker stack deploy -c stack.yml bp-geo