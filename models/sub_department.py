from app import db

class SubDepartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
