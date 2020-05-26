FROM emostudio/server_environment:1.0

RUN pip install nltk

RUN python3 -m nltk.downloader vader_lexicon

ADD * /ml/

WORKDIR /ml

CMD ["python3","application.py"]

