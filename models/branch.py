from app import db
class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # departments = db.relationship('BranchDepartment', backref=db.backref('departments'))
    # departments = db.relationship('Department', secondary='branch_department',
    #                               backref=db.backref('branches', lazy='raise'), lazy='raise')
    departments = db.relationship('Department', secondary='branch_department', lazy='dynamic')
