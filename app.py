#!/usr/bin/env python3

import docker
import yaml
import flask
import flask_caching

# Temporary

top_level_config_key = 'flame'
enable_config_key = 'url'

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

def add_branch(tree, vector, value):
	key = vector[0]
	if len(vector) == 1:
		tree[key] = value  
	else: 
		tree[key] = add_branch(tree[key] if key in tree else {}, vector[1:], value)
	return tree

def get_containers():
	return client.containers.list(filters={'label': top_level_config_key + '.' + enable_config_key, 'status': 'running'})

@cache.cached(timeout=60, key_prefix='docker_containers')
def gen_container_list():
	containers = {}
	for container in get_containers():
		containers[container.name] = container.labels[top_level_config_key + '.' + enable_config_key]
	return containers

# Routes

@app.route('/')
def homepage():
	homepage = "<ul>"
	for name, url in gen_container_list().items():
		homepage += '<li><a href="' + url + '">' + name + '</a></li>'
	homepage += "</ul>"
	return homepage

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8000, debug=True)
else:
	gunicorn_logger = logging.getLogger('gunicorn.error')
	app.logger.handlers = gunicorn_logger.handlers
	app.logger.setLevel(gunicorn_logger.level)
