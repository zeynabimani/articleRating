FROM    python:3.11

RUN     apt-get -qq update

WORKDIR /articleVoter/

ADD     ./requirements.txt .
RUN     pip install -r ./requirements.txt

ADD     . .

# TODO: run this with the help of celery -> python manage.py insert_vote_from_kafka 
CMD     python manage.py migrate && python manage.py runserver 0.0.0.0:8000
