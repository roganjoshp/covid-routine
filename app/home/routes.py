from flask import request, jsonify, render_template, redirect, url_for

from app import db

from app.home import bp
from app.util import WEEKDAYS

from flask_login import login_required


@bp.route('/', methods=['GET'])
@login_required
def homepage():
    return render_template('home/homepage.html')


