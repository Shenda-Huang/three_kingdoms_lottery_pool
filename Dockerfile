FROM python:3.11

COPY requirements.txt requirements-dev.txt /tmp/
RUN python3.11 -m pip install -r /tmp/requirements-dev.txt && \
    mkdir -p /bb/logs

WORKDIR /workspace