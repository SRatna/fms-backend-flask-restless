from flask_restless import APIManager, ProcessingException
from flask import request, jsonify
from app import app, db, bcrypt
from models.admin import Admin
from models.user import User
from models.punch_record import PunchRecord
from models.branch import Branch
from models.department import Department
from models.sub_department import SubDepartment
from models.designation import Designation
from models.grade import Grade
from models.mode import Mode
from models.status import Status
from models.type import Type
from models.employee import Employee


def auth_func(*args, **kwargs):
    auth_token = request.headers.get('auth-token')
    print(auth_token)
    user_id = Admin.decode_auth_token(auth_token)
    print(user_id)
    user = Admin.query.filter_by(id=user_id).first()
    if not user:
        raise ProcessingException(description='Not authenticated!', code=401)
    return True

# manager = APIManager(app, flask_sqlalchemy_db=db, preprocessors=dict(GET_MANY=[auth_func]))
manager = APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(User, methods=['GET'])
manager.create_api(Branch, methods=['GET', 'POST'])
manager.create_api(Department, methods=['GET', 'POST'])
manager.create_api(SubDepartment, methods=['GET', 'POST'])
manager.create_api(Designation, methods=['GET', 'POST'])
manager.create_api(Grade, methods=['GET', 'POST'])
manager.create_api(Mode, methods=['GET', 'POST'])
manager.create_api(Status, methods=['GET', 'POST'])
manager.create_api(Type, methods=['GET', 'POST'])
manager.create_api(Employee, methods=['GET', 'POST'])
manager.create_api(PunchRecord, methods=['GET', 'POST'])


@app.route('/login', methods=['POST'])
def login():
    email, password = request.get_json()['email'], request.get_json()['password']
    user = Admin.query.filter_by(email=email).all()
    if len(user) > 0:
        password_matched = bcrypt.check_password_hash(user[0].password, password)
        print(user[0].id)
        print(Admin.encode_auth_token(user[0].id))
        access_token = {"token": Admin.encode_auth_token(user[0].id).decode('utf-8')}
        print(password_matched)
        return jsonify(access_token)
    else:
        return 'not found'


@app.route('/dashboard', methods=['POST'])
def dashboard():
    posted_date = request.get_json()['date']
    total_registered_users = User.query.count()
    total_present_users = PunchRecord.query.filter_by(date_only=posted_date).group_by(PunchRecord.user_id).count()
    data_to_be_sent = {
        "total_registered_users": total_registered_users,
        "total_present_users": total_present_users
    }
    return jsonify(data_to_be_sent)

@app.after_request
def apply_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'content-type'
    return response

if __name__ == '__main__':
    app.run(
        host='192.168.1.124',
        port=9090
    )
