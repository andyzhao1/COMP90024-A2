# COMP90024-A2-Group55
Team Members:
* [Chuanru Wan - 1074738](https://github.com/EMOSAMA)
* [Shengzhe Zhao - 1074171](https://github.com/andyzhao1)
* [Zhijun Hu - 1094242](https://github.com/zkzzzkz)
* [Sejin Kim - 1025560](https://github.com/s-kim333)
* [Rajeong Moon - 972583](https://github.com/rajeong)


## Video links
### Ansible 
* Part 1: https://youtu.be/_D38VT2fbOc
* Part 2: https://youtu.be/Xdya6DEyqS0
### Frontend presentation

### PowerPoint

## System Structure
![](https://github.com/andyzhao1/COMP90024-A2/blob/master/img/system_structure.png "System Structure")

### Frontend (https://youtu.be/_D38VT2fbOc)
<p>For visualizing analyzed data, we choose Vue which is a components-based development framework to build our web application. Four main packages were used here, the first one is Vue-ElementUI which offers a set of created components and UIs. We have used it to construct the  main structure and style of web pages like Navigation Side Bar and Message Box. The second is Vue-Echart which can be used to draw charts like histogram, pie chart and line chart. The third one is Vue-GoogleMaps, we used it to show data distribution on specific areas. For example, we distribute areas as seven levels based on the num of negative job related tweets and label these areas by seven different colors. The last one is Axios which can be used to communicate with backend servers by HTTP Requests.</p>

### Backend
1. Harvester Server
2. Data Server
3. Semantic Analysis Server
4. Trigger Server

#### Harvester server
<p>We have built APIs for stream tweets and search tweets. The user  can simply call these two APIs to add new thread for harvest tweets.</p>

![](https://github.com/andyzhao1/COMP90024-A2/blob/master/img/harvester_server.png "Harvester Server")

#### Semantic Analysis Server
<p>In this server, we use the SentimentIntensityAnalyzer model under the NLTK package of python. It is a pre-trained natural language processing model which can divide emotions expressed in words into negative or positive. This server can be automatically triggered per hour, and then it will pull tweets from created views on couchdb and label these tweets as negative or positive. Finally it will count the num of negative tweets and positive tweets and  the statistical results will be stored or updated into couchdb. This server is listening on port 5001.</p>

#### Data Server
<p>This server provides main api services for the web application. The Flask which is a lightweight development framework of Python is used here. The couchdb package is used to communicate with the couchdb database. There are two types of services which are Aurin Data Services and Couchdb Data Services. The Aurin Data Services will be listening for requests, once accepting requests, they will read json files which download from Aurin and format them and send the formatted data back as response. The Couchdb Data Services are similar to The Aurin Data Service, but they will return data which come from the couchdb database. This server is listening on port 5000.</p>

#### Trigger Server
<p>If we want to scale up the container of  Harvester Server and Semantic Analysis Server to raise system efficiency, we have to make sure each container operates different tasks. So, we have built a trigger that will automatically allocate tasks by sending requests to the Harvester Server cluster and Semantic Analysis Server cluster. After the requests arrive the docker swarm load balance of both servers, the load balancers can evenly distribute tasks into each container. The trigger will allocate new tasks for collecting latest tweets to Harvester Server per day. And it will assign tasks of analyzing tweets for scenarios to Semantic Analysis Server per hour. The trigger also provides APIs for webapp to manually edit the tasks lists. Generally, users can add new tasks into the task list and also delete tasks from the task list through the web app.</p>

### Database
CouchDB (MapReduce)

## Specfic Code Description
### Twitter harvester
1. Twitter API
2. tweepy streaming
3. Trigger periodically to collect data (once a day)

### Machine learning algorithm
1. Model: SentimentIntensityAnalyzer
2. Trigger periodically to analyze data (one an hour)

### Deployment Operation 
1. Ansible creates 4 instances
2. Ansible deploys 3 CouchDB in instances 1-3 as a cluster
3. Ansible controls Docker-compose with services on each instances 

## Dockerfile
### Images on DockerHub
1. [Web app image](https://hub.docker.com/repository/docker/emostudio/webapp)
2. [Environment (with required python package) image](https://hub.docker.com/repository/docker/emostudio/server_environment)
3. [Harvester Server image](https://hub.docker.com/repository/docker/emostudio/harvester)
4. [Data Server image](https://hub.docker.com/repository/docker/emostudio/server)
5. [Semantic Analysis Server image](https://hub.docker.com/repository/docker/emostudio/machine_learning)
6. [Trigger Server image](https://hub.docker.com/repository/docker/emostudio/trigger)

## Instances information
* Instance1: [172.26.132.195](172.26.132.195:8080)
* Instance2: [172.26.129.104](172.26.129.104:8080)
* Instance3: [172.26.130.101](172.26.130.101:8080)
* Instance3: [172.26.129.79](172.26.129.79:8080)