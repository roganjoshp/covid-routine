from flask import request, jsonify, render_template, redirect, url_for

from app import db

from app.core import bp
from app.util import WEEKDAYS

from app.core.models import Departments

from flask_login import login_required


@bp.route('/', methods=['GET'])
@login_required
def homepage():
    return render_template('core/homepage.html')



