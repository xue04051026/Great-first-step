# 导入Flask核心模块和相关组件
from configparser import BasicInterpolation
from flask import Flask, render_template
# 导入Flask核心模块和相关组件
from flask import Flask, render_template, session, redirect, url_for,flash
from flask_bootstrap import Bootstrap  # 导入Bootstrap扩展
from flask_wtf import FlaskForm  # 导入表单处理模块
from wtforms import StringField, SubmitField ,BooleanField,IntegerField,SelectField, PasswordField  # 导入表单字段类型
from wtforms.validators import DataRequired, Email, EqualTo  # 导入表单验证器
from flask_sqlalchemy import SQLAlchemy  # 导入SQLAlchemy数据库扩展
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user  # 导入Flask-Login模块
from functools import wraps
from flask import abort
from werkzeug.security import generate_password_hash, check_password_hash  # 导入密码加密模块

# 初始化Flask应用实例
app = Flask(__name__)
bootstrap = Bootstrap(app)  # 初始化Bootstrap扩展

app.config['SECRET_KEY'] = 'xxx'  # 配置CSRF保护密钥
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:142857xyp@localhost:3306/studentinfo'
db=SQLAlchemy(app)

# 初始化Flask-Login
login_manager = LoginManager()# 初始化Flask-Login扩展
login_manager.init_app(app)# 初始化Flask-Login扩展
login_manager.login_view = 'login'  # 设置登录页面路由
login_manager.login_message = '请先登录以访问此页面。'  # 设置登录提示消息

# 用户加载回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 管理员权限装饰器
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        if not current_user.is_admin():
           return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# 用户模型
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

class basicInfo(db.Model):
    __tablename__='basicinfo'
    id=db.Column(db.Integer,primary_key=True)
    studentName=db.Column(db.String(255))
    studentBirthday=db.Column(db.String(255))
    isMale=db.Column(db.Boolean)
    studentAge=db.Column(db.Integer)
    major_id = db.Column(db.Integer, db.ForeignKey('majors.id'))

class NameForm(FlaskForm):
    id=StringField('学号')
    name=StringField('请输入姓名：')
    birthday=StringField('请输入出生日期：')
    isMale=BooleanField('是否为男性')
    age=IntegerField('年龄：')
    submit=SubmitField('提交')
    major = SelectField('Major', coerce=int)
class EditForm(NameForm):
    submit = SubmitField("Edit")

# 登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

# 注册表单
class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField(
        '确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册') 
    

    
   
# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(LoginName=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码无效')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash(f'你好，{user.LoginName}!')
        return redirect(url_for('index'))
    return render_template('login.html', title='登录', form=form)

# 注册路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(LoginName=form.username.data).first()
        if existing_user:
            flash('用户名已存在')
            return redirect(url_for('register'))
        user = User(LoginName=form.username.data, role='guest')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜，您已成功注册！')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)

# 注销路由
@app.route('/logout')
def logout():
    logout_user()
    flash('您已成功注销。')
    return redirect(url_for('index'))

# 定义首页路由
@app.route('/')
@login_required
def index():
   studs=basicInfo.query.all()#查询
   majors = Major.query.all() # 查询所有专业
   return render_template('index.html',studs=studs, majors=majors) 

  

# 带参数的路由示例
@app.route('/new',methods=['GET','POST'])
@admin_required
def new_stud():
    form=NameForm()
    form.major.choices = [(m.id, m.major_name) for m in Major.query.order_by('major_name').all()]
    if form.validate_on_submit():
        id = form.id.data
        name = form.name.data
        birthday = form.birthday.data
        isMale = form.isMale.data
        age = form.age.data
        # 通过ID获取选择的 Major 对象
        major_obj = Major.query.get(form.major.data)
        newstud = basicInfo(id=id, studentName=name, studentBirthday=birthday, isMale=isMale, studentAge=age, major=major_obj) # 使用 major 属性关联
        db.session.add(newstud)
        db.session.commit() 
        flash("a new student record is saved") 
        return redirect(url_for('index')) 
    return render_template("new_stud.html",form=form) 

@app.route('/edit/<string:stud_id>',methods=['GET','POST'])
@admin_required
def edit_stud(stud_id):
    form=EditForm()
    stud = basicInfo.query.get(stud_id)
    # 同样需要动态填充选项
    form.major.choices = [(m.id, m.major_name) for m in Major.query.order_by('major_name').all()]
    if form.validate_on_submit():
        stud.id=form.id.data
        stud.studentName = form.name.data
        stud.studentBirthday = form.birthday.data
        stud.isMale = form.isMale.data
        stud.studentAge = form.age.data
        stud.major = Major.query.get(form.major.data) # 更新关联
        db.session.commit() 
        flash('The record is updated') 
        return redirect(url_for('index'))
    form.id.data=stud.id
    form.name.data = stud.studentName
    form.birthday.data = stud.studentBirthday
    form.isMale.data = stud.isMale
    form.age.data = stud.studentAge
    # 页面加载时，设置下拉框的默认选中项
    if stud.major:
        form.major.data = stud.major_id
    return render_template('edit_stud.html',form=form) # 注意使用修复后的模板名

    

# 支持GET/POST方法的表单处理路由
@app.route('/delete/<string:stud_id>', methods=['GET', 'POST'])
@admin_required
def del_stud(stud_id):
    stud=basicInfo.query.get(stud_id)
    
    db.session.delete(stud)
    db.session.commit()
    flash('学生信息删除成功')
    return redirect(url_for('index'))

class Major(db.Model):
    __tablename__='majors'
    id=db.Column(db.Integer,primary_key=True)
    major_name=db.Column(db.String(255),unique=True,nullable=False)
    students = db.relationship('basicInfo', backref='major', lazy='dynamic')
    def __repr__(self):
        return f'<Major {self.major_name}>'
@app.route("/major/<int:major_id>")
def filter_by_major(major_id):
    # 找到被点击的专业
    major = Major.query.get_or_404(major_id)
    # 使用 'major' 关系的反向查询 'students'
    studs = major.students.all()
    # 复用 index.html 模板，但只传入筛选后的学生
    majors = Major.query.all() # 筛选页面也需要专业列表
    return render_template('index.html', studs=studs, majors=majors)


def create_tables():
    """创建数据库表"""
    with app.app_context():
        db.create_all()

# 主程序入口
if __name__ == '__main__':
    # 创建数据库表
    create_tables()
    # 启动开发服务器，开启调试模式
    app.run(debug=True)  # debug=True启用自动重载和调试器
    #stud1 =basicInfo(id=5,studentName='孙七',studentBirthday='20060707',isMale=0,studentAge=19)
   # db.session.add(stud1)
   # db.session.commit()
   #stud =basicInfo(id='8',studentName='test',studentBirthday='20060808',isMale=0,studentAge=19)
   