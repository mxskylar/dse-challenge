FROM python:3.13.5-alpine3.22

WORKDIR /dse-challenge
COPY . /dse-challenge
RUN pip install -r requirements.txt
