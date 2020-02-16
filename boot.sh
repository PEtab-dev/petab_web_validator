#!/bin/sh
source venv/bin/activate
exec gunicorn -b :5000 --access-logfile - --error-logfile - petab_web_validator:app
