#!/bin/bash
# pull frontend
git -C ../frontend pull

# pull backend
git pull

# build images
docker-compose -f production.yml build

# run migrations, if any
docker-compose -f production.yml run --rm django python manage.py migrate

# restart docker
docker-compose  -f production.yml down
docker-compose -f production.yml up -d
