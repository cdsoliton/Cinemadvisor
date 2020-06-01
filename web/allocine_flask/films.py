# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 15:06:45 2020

@author: cdekeyser
"""

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort

from allocine_flask.mongo_client import get_mongo_client

import datetime
from dateutil.relativedelta import relativedelta

from bson.objectid import ObjectId

bp = Blueprint('films', __name__)

@bp.route('/')
def index():
    mongo_client = get_mongo_client()
    mongo_db = mongo_client[current_app.config["MONGO_DB"]]
    limit_date = datetime.datetime.today() + relativedelta(days=-1*int(current_app.config["MAX_FETCH_DAYS"]))
    dummy_id = ObjectId.from_datetime(limit_date)
    films = mongo_db[current_app.config["MONGO_COLL"]].find({"_id": {"$gt": dummy_id}})
    return render_template('films/index.html', films=films)