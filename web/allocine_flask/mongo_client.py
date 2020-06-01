# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 14:14:46 2020

@author: cdekeyser
"""

import pymongo

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_mongo_client():
    
    if 'mongo_client' not in g:
        g.mongo_client = pymongo.MongoClient(current_app.config['MONGO_CLIENT'])

    return g.mongo_client


def close_mongo_client(e=None):
    
    mongo_client = g.pop('mongo_client', None)

    if mongo_client is not None:
        mongo_client.close()