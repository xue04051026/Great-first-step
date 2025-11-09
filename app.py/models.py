from . import db  # 稍后在 __init__.py 中定义 db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# (注意：login_manager.user_loader 也会移到这里或 __init__)
from .import login_manager # 稍后在 __init__.py 中定义 login_manager
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    LoginName = db.Column(db.String(80), unique=True, nullable=False)
    Password = db.Column(db.String(128))
    role = db.Column(db.String(20), default='guest')  # 角色字段：admin 或 guest
    
    def set_password(self, password):
        self.Password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.Password, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Major(db.Model):
    __tablename__='majors'
    id=db.Column(db.Integer,primary_key=True)
    major_name=db.Column(db.String(255),unique=True,nullable=False)
    students = db.relationship('basicInfo', backref='major', lazy='dynamic')

class basicInfo(db.Model):
    __tablename__='basicinfo'
    id=db.Column(db.Integer,primary_key=True)
    studentName=db.Column(db.String(255))
    studentBirthday=db.Column(db.String(255))
    isMale=db.Column(db.Boolean)
    studentAge=db.Column(db.Integer)
    major_id = db.Column(db.Integer, db.ForeignKey('majors.id'))
    

