from app import db
from models.employee import Employee

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    @classmethod
    def query(cls):
        original_query = db.session.query(cls)
        registered_user_ids = db.session.query(Employee.user_id)
        return original_query.filter(User.id.notin_(registered_user_ids))