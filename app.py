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
