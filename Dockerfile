FROM ubuntu:20.04 as base

USER root
RUN apt-get update
RUN apt-get -y install curl gnupg
RUN apt-get --assume-yes -q install python3.8 python3-pip python3.8-dev libpq-dev
RUN alias python3=python3.8

RUN curl -sL https://deb.nodesource.com/setup_16.x  | bash -
RUN apt-get -y install nodejs

RUN rm -rf /var/lib/apt/lists/ /var/cache/apt/

# These invalidate the cache every single time but
# there really isn't any other obvious way to do this.
COPY . /app
WORKDIR /app

RUN pip3 install -U pip
RUN pip3 install -U setuptools
RUN pip3 install -r requirements-dev.txt
