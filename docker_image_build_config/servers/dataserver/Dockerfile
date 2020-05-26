FROM emostudio/server_environment:1.0

ADD ../../../servers/dataserver/* /dataserver/
ADD ../../../servers/dataserver/JSON /dataserver/JSON
WORKDIR /dataserver

CMD ["python3","application.py"]
