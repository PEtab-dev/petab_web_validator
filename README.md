# petab_web_validator

[PEtab](https://github.com/petab-dev/petab) validation web service.


# Install and run locally

This web service uses the python web applications framework
[flask](https://flask.palletsprojects.com/en/1.1.x/).

Install the requirements defined in `requirements.txt`. In particular, these
include `flask flask-wtf flask-bootstrap` as well as `petab` of course, which
can all be installed using `pip install`.

To run the service locally, in the command line clone the project folder, e.g.
via

    git clone https://github.com/petab-dev/petab_web_validator
    cd petab_web_validator

and then

    export FLASK_APP=app
    flask run
