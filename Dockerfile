# VERSION 1.10.3
# AUTHOR: Matthieu "Puckel_" Roisil
# DESCRIPTION: Basic Airflow container
# BUILD: docker build --rm -t puckel/docker-airflow .
# SOURCE: https://github.com/puckel/docker-airflow

FROM python:3.6-slim-stretch
LABEL maintainer="Puckel_"

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Airflow
ARG AIRFLOW_VERSION=1.10.3
ARG AIRFLOW_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS=""
ARG BUILD_DEPS=" \
    freetds-bin \
    build-essential \
    apt-utils \
    curl \
    rsync \
    netcat \
    locales \
    "

# Define en_US.
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV AIRFLOW_HOME /usr/local/airflow

RUN set -ex \
    && buildDeps=" \
    freetds-dev \
    libkrb5-dev \
    libsasl2-dev \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    git \
    " \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
    $buildDeps \
    $BUILD_DEPS \
    && localedef -f UTF-8 -i en_US en_US.UTF-8 \
    && pip install -U pip setuptools wheel \
    && pip install email_validator \
    && pip install pytz \
    && pip install pyOpenSSL \
    && pip install ndg-httpsclient \
    && pip install pyasn1 \
    && pip install Flask==1.0.4 \
    && pip install 'tzlocal<2.0.0.0, >=1.5.0.0' \
    && pip install apache-airflow[crypto,postgres,ssh${AIRFLOW_DEPS:+,}${AIRFLOW_DEPS}]==${AIRFLOW_VERSION} \
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
    /var/lib/apt/lists/* \        
    /root/.cache/pip/* \
    /tmp/* \
    /var/tmp/* 

COPY script/entrypoint.sh /entrypoint.sh
COPY requirements.txt /requirements.txt
COPY config/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

EXPOSE 8080 5555 8793

WORKDIR ${AIRFLOW_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"] # set default arg for entrypoint
