from flask import current_app

from app import db
from app.util import natural_keys

from enum import IntEnum

import datetime as dt


class Departments(db.Model):
    """ Freetext definition of the department name
    
    Departments are the highest-level objects of the system. Ultimately, all
    objects e.g. constraints and staff must be associated directly or 
    indirectly with a particular department
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    
    @staticmethod
    def get_all():
        depts = Departments.query.order_by('name').all()
        return depts

    @staticmethod
    def create_new(name):
        exists = Departments.query.filter_by(name=name).all()
        if exists is not None:
            return {'status': False,
                    'message': 'Department name already exists'}
        
        dept = Departments(name=name)
        db.session.add(dept)
        db.session.commit()
        return {'status': True,
                'message': 'Success'}


class DepartmentConstraintTypes(IntEnum):
    must_have = 1
    must_not_have = 2
    nice_to_have = 3
    
    @staticmethod
    def get_all():
        constraint_list = []
        for name, number in DepartmentConstraintTypes.__members__.items():
            constraint_list.append([number.value, name.replace('_', ' ')])
        return constraint_list


class DepartmentSkillConstraints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer,
                              db.ForeignKey('departments.id',
                                            ondelete='CASCADE'))
    skill_id = db.Column(db.Integer,
                         db.ForeignKey('skills.id',
                                       ondelete='CASCADE'),
                         index=True)
    level = db.Column(db.Integer)
    start_day = db.Column(db.Integer)
    start_hour = db.Column(db.Integer)
    end_day = db.Column(db.Integer)
    end_hour = db.Column(db.Integer)
    is_permanent = db.Column(db.Boolean) # Applies all week
    
    # Pseudo ForeignKey to DepartmentConstraintTypes
    constraint_type_id = db.Column(db.Integer) 
    
    @staticmethod
    def get_all():
        pass


class Staff(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id',
                                      ondelete='SET NULL'))
    department_id = db.Column(db.Integer,
                              db.ForeignKey('departments.id',
                                            ondelete='CASCADE'),
                              index=True)
    department = db.relationship('Departments')
    name = db.Column(db.String(50))
    skills = db.relationship('Skills', secondary='staff_skills',
                             backref=db.backref('staff', lazy='dynamic'),
                             lazy='dynamic')
    is_reserve = db.Column(db.Boolean) # Active staff or reserve
    
    @staticmethod
    def get_all(dept_id=None):
        
        staff = db.session.query(Staff)
        if dept_id is not None:
            staff = (staff.join(Departments)
                          .filter(Departments.id==int(dept_id)))
        staff = staff.all()
        staff.sort(key=lambda x: natural_keys((x.name)))
        return staff


class Skills(db.Model):
    """ Free-text name of skills that staff can possess """
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    
    @staticmethod
    def get_all():
        skills = Skills.query.all()
        skills.sort(lambda x: natural_keys(x))
        return skills


staff_skills = db.Table('staff_skills',
                        db.Column('staff_id',
                                  db.Integer,
                                  db.ForeignKey('staff.id'),
                                  primary_key=True),
                        db.Column('skill_id',
                                  db.Integer,
                                  db.ForeignKey('skills.id'),
                                  primary_key=True)
                        )


class StaffShiftConstraints(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer,
                         db.ForeignKey('staff.id',
                                       ondelete='CASCADE'),
                         index=True)
    day_number = db.Column(db.Integer)
    min_start_hour = db.Column(db.Integer)
    max_start_hour = db.Column(db.Integer)
    min_shift_hours = db.Column(db.Integer)
    max_start_hour = db.Column(db.Integer)
    min_shift_gap = db.Column(db.Integer)
    
    @staticmethod
    def get_all(staff_id):
        constraints = (StaffShiftConstraints.query
                                            .filter_by(staff_id=int(staff_id))
                                            .order_by('day_number')
                                            .all())
        return constraints
    

class WeeklyMaxHours(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer,
                         db.ForeignKey('staff.id',
                                       ondelete='CASCADE'),
                         index=True)
    hours = db.Column(db.Integer)