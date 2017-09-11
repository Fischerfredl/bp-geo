#!/usr/bin/env bash

docker build -t fischerfredl/bp-geo:development .
docker push fischerfredl/bp-geo:development
docker stack deploy -c stack.yml bp-geo