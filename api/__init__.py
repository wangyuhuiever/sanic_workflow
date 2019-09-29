# -*- coding: utf-8 -*-

from sanic import Blueprint
from .app import app

api = Blueprint.group(app, url_prefix='/api')