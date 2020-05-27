# Web App Image
## Description
This is a docker image for frontend web app.
## Build image
```
docker build -t emostudio/webapp:latest .
```
## Run image
```
docker run -d -p 8080:8080 --name webapp emostudio/webapp:latest
```