from app import db

class Designation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))