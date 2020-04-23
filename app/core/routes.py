from flask import request, jsonify, render_template, redirect, url_for

from app import db

from app.core import bp
from app.util import handle_ajax_error

from app.auth.models import group_required
from app.core.models import Departments

from flask_login import login_required


@bp.route('/', methods=['GET'])
@login_required
def homepage():
    return render_template('core/homepage.html')


@bp.route('/departments', methods=['GET'])
@login_required
def departments_home():
    departments = Departments.get_all()
    return render_template('core/departments/homepage.html',
                           departments=departments)
    
    
@bp.route('/create_department', methods=['POST'])
@login_required
def create_department():
    
    req = request.form.to_dict()
    dept_name = req.get('department_name')
    rtn = {}
    
    if not dept_name:
        rtn= {'status': False,
              'message': 'No department name specified'}
    
    try:
        rtn = Departments.create_new(dept_name)
    except Exception as e:
        rtn = {'status': False,
               'message': 'Unknown exception occurred'}
    
    rtn = handle_ajax_error(rtn)
    
    return jsonify(rtn)