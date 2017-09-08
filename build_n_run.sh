#!/usr/bin/env bash

docker build -t bp-geo .
# docker push fischerfredl/bp-geo:latest
# docker stack deploy -c stack.yml bp-geo