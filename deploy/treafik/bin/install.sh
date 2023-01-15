#!/usr/bin/env bash

# Create docker networks (fails if exists)
docker network create web
clear

# Make acme file for SSL
if test -f "./acme.json"; then
    echo "acme.json already exists, will not over-ride it!"
else
    # Create ssl file (empty) and give correct permission
    touch acme.json
    chmod 600 acme.json
fi

# Pull Images
docker-compose -f docker-compose.yml pull
