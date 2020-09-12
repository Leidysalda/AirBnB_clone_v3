#!/usr/bin/python3
"""Import Blueprint"""
from flask import Blueprint
from models.city import City
from models.state import State

app_views = Blueprint('index', __name__, url_prefix='/api/v1/')
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
