# Semantic analysis server Image
## Description
This is a docker image for semantic analysis server in backend.
## Build image
```
docker build -t emostudio/machine_learning:latest .
```
## Run image
```
docker run -d -p 5002:5002 --name ml emostudio/machine_learning:latest
```