#!/bin/bash
set -e

printf "creating single network --->\n"
docker network create api_db;
printf "network single created --->\n"

cd db;

printf "starting db container --->\n"
docker container run \
    --detach \
    --publish=3001:3306 \
    --name=db \
    --env-file db.env \
    --network=api_db \
    mysql:latest;
printf "db container started --->\n"

printf "\n"

cd ..

cd api;
printf "creating api image --->\n"
docker image build . --tag crudim;
printf "api image created --->\n"
printf "starting api container --->\n"
docker container run \
    --detach \
    --publish=8000:5000 \
    --name=api \
    --env-file api.env \
    --network=api_db \
    crudim;
docker container exec api flask db init;
docker container exec api flask db migrate -m "Initial migration";
docker container exec api flask db upgrade;
printf "api container started --->\n"

cd ..
printf "\n"

printf "all containers are up and running"