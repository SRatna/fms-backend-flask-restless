from app import db,app
from models.admin import Admin
from flask_script import Manager
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

manager = Manager(app)

@manager.command
def create_db():
    db.create_all()

@manager.command
def create_admin():
    admin = Admin(
        email='admin@gmail.com',
        password='admin'
    )
    db.session.add(admin)
    db.session.commit()

if __name__ == "__main__":
    manager.run()
