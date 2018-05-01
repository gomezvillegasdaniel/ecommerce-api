## How to setup the development environment:

- Create a volume for the datababase
```
docker volume create --name=db_data
```

- Build the docker image and service
```
docker-compose build web
```

- Start the container as a daemon service
```
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
docker-compose up test
```