# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 13:58:51 2020

@author: cdekeyser
"""

import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        MONGO_CLIENT = "mongodb+srv://soliton:instantsia@solitontest-mmj4o.azure.mongodb.net/?retryWrites=true&w=majority",
        MONGO_DB = "allocine",
        MONGO_COLL = "films",
        MAX_FETCH_DAYS = "40"
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import films
    app.register_blueprint(films.bp)
    app.add_url_rule('/', endpoint='index')


    return app