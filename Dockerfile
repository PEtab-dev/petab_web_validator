FROM python:3.6-alpine

RUN adduser -D petab_web_validator

WORKDIR /home/petab_web_validator

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY petab_web_validator.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP petab_web_validator.py

RUN chown -R petab_web_validator:petab_web_validator ./
USER petab_web_validator

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]

