#!/usr/bin/python3
"""Import Blueprint"""
from flask import Blueprint


app_views = Blueprint('index', __name__, url_prefix='/api/v1/')
import api.v1.views.index
from api.v1.views.states import *
