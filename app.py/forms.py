from flask_wtf import FlaskForm  # 导入表单处理模块
from wtforms import StringField, SubmitField ,BooleanField,IntegerField,SelectField, PasswordField  # 导入表单字段类型
from wtforms.validators import DataRequired, Email, EqualTo  # 导入表单验证器

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