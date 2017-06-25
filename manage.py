from app import db,app
from models.admin import Admin
from flask_script import Manager
from models.department import Department
from models.sub_department import SubDepartment

manager = Manager(app)

@manager.command
def create_db():
    db.create_all()

@manager.command
def create_admin():
    admin = Admin(
        email='sunamjohn@gmail.com',
        password='admin'
    )
    db.session.add(admin)
    db.session.commit()

if __name__ == "__main__":
    manager.run()