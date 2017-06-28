from app import db

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    sub_departments = db.relationship('SubDepartment', secondary='department_sub_department', lazy='dynamic')
