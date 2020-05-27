# Data server Image
## Description
This is a docker image for data server in backend.
## Build image
```
docker build -t emostudio/server:latest .
```
## Run image
```
docker run -d -p 5000:5000 --name server emostudio/server:latest
```