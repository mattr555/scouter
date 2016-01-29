#!/usr/bin/env python

import os
import readline
from pprint import pprint
from app import db, app
from models import *

db.app=app

os.environ['PYTHONINSPECT'] = 'True'

us = Team.query.filter_by(license='765A').first()

def t(l):
    return Team.query.filter_by(license=l).first()
