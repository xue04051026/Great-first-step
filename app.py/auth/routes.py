from flask import render_template, redirect, url_for, flash, request
from . import auth  # 导入当前蓝图实例
from .. import db    # 导入 app 实例
from ..models import User
from ..forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, login_required


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(LoginName=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码无效')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        flash(f'你好，{user.LoginName}!')
        return redirect(url_for('main.index'))
    return render_template('login.html', title='登录', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(LoginName=form.username.data).first()
        if existing_user:
            flash('用户名已存在')
            return redirect(url_for('auth.register'))
        user = User(LoginName=form.username.data, role='guest')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜，您已成功注册！')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='注册', form=form)

# 注销路由
@auth.route('/logout')
def logout():
    logout_user()
    flash('您已成功注销。')
    return redirect(url_for('main.index'))