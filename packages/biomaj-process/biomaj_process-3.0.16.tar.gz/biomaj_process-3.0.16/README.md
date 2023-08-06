# About

[![PyPI version](https://badge.fury.io/py/biomaj-process.svg)](https://badge.fury.io/py/biomaj-process)

Microservice to manage the process execution of biomaj.

A protobuf interface is available in biomaj_process/message/message_pb2.py to exchange messages between BioMAJ and the download service.
Messages go through RabbitMQ (to be installed).

# Protobuf

To compile protobuf, in biomaj_process/message:

    protoc --python_out=. message.proto

# Development

    flake8  biomaj_process

# Run

## Message consumer:
export BIOMAJ_CONFIG=path_to_config.yml
python bin/biomaj_process_consumer.py

## Web server

If package is installed via pip, you need a file named *gunicorn_conf.py* containing somehwhere on local server:

    def worker_exit(server, worker):
        from prometheus_client import multiprocess
        multiprocess.mark_process_dead(worker.pid)

If you cloned the repository and installed it via python setup.py install, just refer to the *gunicorn_conf.py* in the cloned repository.


    export BIOMAJ_CONFIG=path_to_config.yml
    rm -rf ..path_to/prometheus-multiproc
    mkdir -p ..path_to/prometheus-multiproc
    export prometheus_multiproc_dir=..path_to/prometheus-multiproc
    gunicorn -c ..path_to/gunicorn_conf.py biomaj_download.biomaj_process_web:app

Web processes should be behind a proxy/load balancer, API base url /api/process

A prometheus /metrics endpoint is exposed on web server
