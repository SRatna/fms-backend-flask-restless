from app import db

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)
    # branch = db.relationship('Branch', backref=db.backref('departments', lazy=True))
    branch = db.relationship('Branch')