FROM    python:3.11

RUN     apt-get -qq update

WORKDIR /articleVoter/

ADD     ./requirements.txt .
RUN     pip install -r ./requirements.txt

ADD     . .

RUN     python manage.py migrate
CMD     python manage.py runserver 0.0.0.0:8000
