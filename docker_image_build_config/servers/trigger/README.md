# Trigger server Image
## Description
This is a docker image for trigger server in backend.
## Build image
```
docker build -t emostudio/trigger:latest .
```
## Run image
```
docker run -d -p 5003:5003 --name trigger emostudio/trigger:latest
```