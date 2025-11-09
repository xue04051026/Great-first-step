from flask import render_template, redirect, url_for, flash, abort
from . import main
from .. import db
from ..models import basicInfo, Major
from ..forms import NameForm, EditForm
from flask_login import login_required, current_user # (用于权限控制)
from functools import wraps

# 管理员权限装饰器
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)  # 禁止访问
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
@login_required
def index():
   studs=basicInfo.query.all()#查询
   majors = Major.query.all() # 查询所有专业
   return render_template('index.html',studs=studs, majors=majors) 

@main.route('/new',methods=['GET','POST'])
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
        return redirect(url_for('main.index')) 
    return render_template("new_stud.html",form=form) 

@main.route('/edit/<string:stud_id>',methods=['GET','POST'])
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
        return redirect(url_for('main.index'))
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
@main.route('/delete/<string:stud_id>', methods=['GET', 'POST'])
@admin_required
def del_stud(stud_id):
    stud=basicInfo.query.get(stud_id)
    
    db.session.delete(stud)
    db.session.commit()
    flash('学生信息删除成功')
    return redirect(url_for('main.index'))

