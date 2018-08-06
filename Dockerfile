FROM python:alpine

RUN pip install pipenv

RUN mkdir /zapi
WORKDIR /zapi

COPY . /zapi/

RUN pipenv install --deploy --system

# FIXME: It's recommended to use uwsgi to run this flaks app in production
ENTRYPOINT ["python", "zapi/main.py"]
