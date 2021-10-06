# syntax=docker/dockerfile:1
FROM python:3.9-bullseye

# We need to install git inorder to pull down the soundcloud lib
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && update-ca-certificates --fresh

## This + `update-ca-certificates --fresh` is needed to make sure the cert store is up to date
# otherwise the bot will fail to verify discords certificate
ENV SSL_CERT_DIR "/etc/ssl/certs"

WORKDIR /app

# install python depdencies
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# copy over the python code
COPY . .

CMD [ "python3", "-u", "main.py"]

