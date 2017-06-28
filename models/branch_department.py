from app import db

class BranchDepartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)
    # branch = db.relationship('Branch', backref=db.backref('departments', lazy=True))
    # if we set backref here than we can get departments from branch table automatically
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    # department = db.relationship('Department', backref=db.backref('branches', lazy=True))
