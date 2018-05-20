[![Build Status](https://travis-ci.org/gomezvillegasdaniel/ecommerce-api.svg?branch=dev)](https://travis-ci.org/gomezvillegasdaniel/ecommerce-api)

## How to setup the development environment:

- Create a volume for the database
```
docker volume create --name=db_data
```

- Build the docker image and service
```
docker-compose build web
```

- Start the container
```
docker-compose up web

You can run it as a daemon service with:
docker-compose up -d web
```

- To get into bash in an existing container already started (optional):
```
docker exec -i -t container_id /bin/bash
```

- To stop the container
```
docker-compose down web
```

- To run tests
```
docker-compose -f docker-compose-test.yml up test
```