## How to setup:

- Create a volume for the datababase
```
docker volume create --name=db_data
```

- Build the docker image and service
```
docker-compose build service_name
```

- Start the container as a daemon service
```
docker-compose up -d service_name
```

- Stop the container (optional)
```
docker-compose down service_name
```

- Get into bash in an existing container already started (optional): 
```
docker exec -i -t container_id /bin/bash
```

- To run tests
```
docker-compose up test
```
