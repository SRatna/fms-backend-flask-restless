from app import db

class PunchRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')
    date_time = db.Column(db.DateTime)
    date_only = db.Column(db.Date)
    time_only = db.Column(db.Time)