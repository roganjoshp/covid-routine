from flask import request, jsonify, render_template, redirect, url_for

from app import db

from app.core import bp
from app.util import format_ajax_message

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
    dept_name = req.get('new_department_name')
    
    if not dept_name:
        rtn= {'status': False,
              'message': 'No department name specified',
              'template': render_template(
                              'core/departments/existing_department_table.html',
                              departments=Departments.get_all())
              }
        return jsonify(format_ajax_meassage(rtn))
    
    try:
        rtn = Departments.create_new(dept_name)
    except Exception as e:
        rtn = {'status': False,
               'message': 'Unknown exception occurred'}
    
    rtn['template'] = render_template(
                              'core/departments/existing_department_table.html',
                              departments=Departments.get_all()
                             )
    
    return jsonify(format_ajax_message(rtn))


@bp.route('/delete_department', methods=['POST'])
@login_required
def delete_department():
    
    req = request.json
    department_id = int(req.get('department_id', 0))
    print("department_id", department_id)
    department = Departments.query.get(department_id)
    if department is not None:
        db.session.delete(department)
        db.session.commit()
    
    return render_template('core/departments/existing_department_table.html',
                            departments=Departments.get_all())