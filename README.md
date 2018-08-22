[![Build Status](https://travis-ci.org/ONSdigital/rasrm-ops.svg?branch=master)](https://travis-ci.org/ONSdigital/rasrm-ops)
# RASRM OPS

## Purpose
A utility tool to support the service operationally. This is intended for developers to use to support RASRM in the
absence of capability in https://github.com/ONSdigital/response-operations-ui

## Requirements
* Docker
* pipenv

## Building
Run `make docker`

## Running
1. Run `make docker-run`
1. Go to http://0.0.0.0:8003/

## Testing
Run `make test`

