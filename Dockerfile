FROM python:3.12-slim-bookworm

WORKDIR /workdir

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && \
    pip install -r requirements.txt

COPY app app

ENV PYTHONPATH=/workdir