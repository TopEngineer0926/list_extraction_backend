# syntax = docker/dockerfile:1.4

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./app ./app

FROM builder as dev-envs

RUN apt-get update
RUN apt-get install -y --no-install-recommends git

RUN useradd -s /bin/bash -m vscode
RUN groupadd docker
RUN usermod -aG docker vscode

# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /

EXPOSE 80