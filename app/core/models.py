from flask import current_app

from sqlalchemy import and_, func, cast, Date

from app import db
from app.util import parse_shift_time, natural_keys, shift_timestamp_to_human

import datetime as dt


class Departments(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    

class StaffSkills(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

