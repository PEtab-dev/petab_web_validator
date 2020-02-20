FROM python:3.8-slim-buster

RUN adduser --disabled-password petab_web_validator

WORKDIR /home/petab_web_validator

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get -y install gcc && apt-get -y install g++
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install --no-cache-dir matplotlib>=2.2.3 pandas>=0.23.4 python-libsbml>=5.17.0
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY petab_web_validator.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP petab_web_validator.py

RUN chown -R petab_web_validator:petab_web_validator ./
USER petab_web_validator

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]

