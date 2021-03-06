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
from models.branch_department import BranchDepartment
from models.department_sub_department import DepartmentSubDepartment
import datetime

fmt = '%Y-%m-%d'  # format for date extraction


def auth_func(*args, **kwargs):
    auth_token = request.headers.get('auth-token')
    print(auth_token)
    user_id = Admin.decode_auth_token(auth_token)
    print(user_id)
    user = Admin.query.filter_by(id=user_id).first()
    if not user:
        raise ProcessingException(description='Not authenticated!', code=401)
    return True


manager = APIManager(app, flask_sqlalchemy_db=db, preprocessors=dict(GET_MANY=[auth_func], POST_MANY=[auth_func],
                                                                     GET=[auth_func], DELETE=[auth_func],
                                                                     DELETE_MANY=[auth_func], POST=[auth_func]))
# manager = APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(User, methods=['GET'], results_per_page=0)
manager.create_api(Branch, methods=['GET', 'POST', 'DELETE', 'PATCH'])
manager.create_api(Department, methods=['GET', 'POST', 'DELETE', 'PATCH'])
manager.create_api(SubDepartment, methods=['GET', 'POST', 'DELETE', 'PATCH'])
manager.create_api(Designation, methods=['GET', 'POST', 'DELETE', 'PATCH'])
manager.create_api(Grade, methods=['GET', 'POST', 'DELETE', 'PATCH'])
manager.create_api(Mode, methods=['GET', 'POST', 'DELETE', 'PATCH'])
manager.create_api(Status, methods=['GET', 'POST', 'DELETE', 'PATCH'])
manager.create_api(Type, methods=['GET', 'POST', 'DELETE', 'PATCH'])
manager.create_api(Employee, methods=['GET', 'POST', 'DELETE', 'PATCH'])
manager.create_api(PunchRecord, methods=['GET', 'POST', 'DELETE', 'PATCH'])
manager.create_api(BranchDepartment, methods=['GET', 'POST', 'DELETE', 'PATCH'])
manager.create_api(DepartmentSubDepartment, methods=['GET', 'POST', 'DELETE', 'PATCH'])

@app.route('/api/alluser', methods=['GET'])
def alluser():
    allusers = db.session.query(User).all()
    totalUserList = []
    for user in allusers:
        totalUserList.append({
            'id': user.id,
            'name': user.name
        })
    # print(allusers)
    return jsonify(totalUserList)
@app.route('/api/login', methods=['POST'])
def login():
    email, password = request.get_json()['email'], request.get_json()['password']
    user = Admin.query.filter_by(email=email).all()
    if len(user) > 0:
        password_matched = bcrypt.check_password_hash(user[0].password, password)
        if password_matched:
            access_token = {"token": Admin.encode_auth_token(user[0].id).decode('utf-8')}
            return jsonify(access_token)
        else:
            error = {"error": "password did not matched"}
            return jsonify(error)
    else:
        error = {"error": "user not found"}
        return jsonify(error)


@app.route('/api/dashboard', methods=['POST'])
def dashboard():
    posted_date = request.get_json()['date']
    working_status_id = db.session.query(Status.id).filter(Status.name.like('working'))
    registered_user_ids = db.session.query(Employee.user_id).filter(Employee.status_id.in_(working_status_id))
    total_registered_users = Employee.query.filter(Employee.status_id.in_(working_status_id)).count()
    total_present_users = PunchRecord.query.filter_by(date_only=posted_date)\
        .filter(PunchRecord.user_id.in_(registered_user_ids))\
        .group_by(PunchRecord.user_id).count()
    data_to_be_sent = {
        "total_registered_users": total_registered_users,
        "total_present_users": total_present_users
    }
    return jsonify(data_to_be_sent)


@app.route('/api/attendance', methods=['POST'])
def attendance():
    global check_in, check_out, formatted_worked_time, status, remarks, formatted_total_worked_time
    user_id = request.get_json()['user_id']
    start_date = request.get_json()['start_date']
    end_date = request.get_json()['end_date']
    start_date_obj = datetime.datetime.strptime(start_date, fmt)
    end_date_obj = datetime.datetime.strptime(end_date, fmt)
    date = start_date_obj
    # initialize an empty total_worked_time
    total_worked_time = datetime.timedelta()
    # initialize an empty array for data to be sent
    attendance_records = []
    while date <= end_date_obj:
        date_string = str(date.date())
        results = PunchRecord.query.filter_by(user_id=user_id).filter_by(date_only=date_string).all()
        if date.weekday() == 5:
            day = 'Saturday'
        else:
            day = 'Working day'
        if len(results) == 0:
            check_in = '00-00-00 00:00:00'
            check_out = '00-00-00 00:00:00'
            formatted_worked_time = '0'
            if date.weekday() == 5:
                status = 'xxx'
            else:
                status = 'Absent'
            remarks = 'xxx'
        if len(results) == 1:
            check_in = results[0].date_time
            check_out = '00-00-00 00:00:00'
            formatted_worked_time = '0'
            status = 'Unknown'
            remarks = 'Forgot to checkout'
        if len(results) == 2:
            check_in = results[0].date_time
            check_out = results[1].date_time
            worked_time = check_out - check_in
            worked_time_str = str(worked_time)
            worked_time_array = worked_time_str.split(':')
            formatted_worked_time = worked_time_array[0] + ' hours ' + worked_time_array[1] + ' minutes ' + \
                                    worked_time_array[2] + ' seconds'
            status = 'Present'
            remarks = 'xxx'
            total_worked_time = total_worked_time + worked_time
        if len(results) > 2:
            check_in = results[0].date_time
            check_out = results[len(results) - 1].date_time
            worked_time = check_out - check_in
            worked_time_str = str(worked_time)
            worked_time_array = worked_time_str.split(':')
            formatted_worked_time = worked_time_array[0] + ' hours ' + worked_time_array[1] + ' minutes ' + \
                                    worked_time_array[2] + ' seconds'
            status = 'Present'
            remarks = 'xxx'
            total_worked_time = total_worked_time + worked_time
        check_in_array = str(check_in).split(' ')
        check_out_array = str(check_out).split(' ')
        attendance_records.append({
            'date': str(date.date()),
            'check_in': check_in_array[1],
            'check_out': check_out_array[1],
            'worked_time': formatted_worked_time,
            'status': status,
            'remarks': remarks,
            'day': day
        })
        date += datetime.timedelta(days=1)
    total_worked_time_str = str(total_worked_time)
    total_worked_time_array = total_worked_time_str.split(':')
    # print(total_worked_time_str)
    days_hours_str = str(total_worked_time_array[0])
    if "days" in days_hours_str:
        days_hours_array = days_hours_str.split(' days, ')
        days_only = int(days_hours_array[0])
        hours_only = int(days_hours_array[1])
        total_hours_in_total_worked_time = days_only * 24 + hours_only
    else:
        total_hours_in_total_worked_time = total_worked_time_array[0]

    formatted_total_worked_time = str(total_hours_in_total_worked_time) + ' hours ' + total_worked_time_array[1] + ' minutes ' + \
                            total_worked_time_array[2] + ' seconds'
    data_to_be_sent = [{
        "attendance_records": attendance_records,
        "total_worked_time": formatted_total_worked_time
    }]
    return jsonify(data_to_be_sent)

@app.after_request
def apply_cors(response):
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'content-type, auth-token'
    return response


if __name__ == '__main__':
    app.run(
        host='192.168.1.189',
        port=9090
    )
