#!/usr/bin/env python3

import docker
import yaml
import flask
import flask_caching
# Static Vars

config = {
	"CACHE_TYPE": "SimpleCache",
	"CACHE_DEFAULT_TIMEOUT": 300
}

# Initialization

client = docker.from_env()
app = flask.Flask(__name__)
app.config.from_mapping(config)
cache = flask_caching.Cache(app)

# Functions

def get_containers():
	return client.containers.list(filters={'label': top_level_config_key + '.' + enable_config_key, 'status': 'running'})

@cache.cached(timeout=60, key_prefix='docker_containers')
def gen_container_list():
	containers = {}
	for container in get_containers():
		containers[container.name] = container.labels[top_level_config_key + '.' + enable_config_key]
	return containers
