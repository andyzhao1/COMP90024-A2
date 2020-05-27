# Harvester server Image
## Description
This is a docker image for harvester server in backend.
## Build image
```
docker build -t emostudio/harvester:latest .
```
## Run image
```
docker run -d -p 5001:5001 --name harvester emostudio/harvester:latest
```