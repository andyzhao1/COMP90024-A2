# COMP90024-A2-Group55

Team Members:
* [Sejin Kim - 1025560]
* [Chuanru Wan - 1074738]
* [Shengzhe Zhao - 1074171]
* [Zhijun Hu - 1094242]
* [Rajeong Moon - 972583]

## Video links
### Ansible
'''
* Part 1: https://youtu.be/_D38VT2fbOc
* Part 2: https://youtu.be/Xdya6DEyqS0
'''
### Frontend presentation
'''
'''
### PowerPoint
'''
'''

## Project Structure
### Frontend
'''
1. Vue
2. Echarts
'''
### Backend
'''
1. harvester server
2. Data server
3. Semantic Analysis Server
4. Trigger
'''
### Database
'''
1. CouchDB (MapReduce)
'''
### Twitter harvester
'''
1. Twitter API
2. tweepy streaming
3. Trigger periodically to collect data (once a day)
'''
### Machine learning algorithm
'''
1. Model: SentimentIntensityAnalyzer
2. Trigger periodically to analyze data (one an hour)
'''
### Deployment Operation 
'''
1. Ansible creates 4 instances
2. Ansible deploys 3 CouchDB in instances 1-3 as a cluster
3. Ansible controls Docker-compose with services on each instances 
'''
### Instances information
'''
Instance1: 172.26.132.195
 
Instance2: 172.26.129.104
 
Instance3: 172.26.130.101
 
Instance3: 172.26.129.79
'''