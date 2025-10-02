# auth_views.py 안
from flask import Blueprint, render_template, redirect, url_for, flash
# from sprout import UserCreateForm, UserLoginForm  ← 제거
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

# 폼 정의
class UserCreateForm(FlaskForm):
    username = StringField("사용자 이름", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("이메일", validators=[DataRequired(), Email()])
    password = PasswordField("비밀번호", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("회원가입")

class UserLoginForm(FlaskForm):
    email = StringField("이메일", validators=[DataRequired(), Email()])
    password = PasswordField("비밀번호", validators=[DataRequired()])
    submit = SubmitField("로그인")

# Blueprint 정의
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = UserCreateForm()
    if form.validate_on_submit():
        flash(f"{form.username.data}님 회원가입 완료!", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        flash(f"{form.email.data} 로그인 성공!", "success")
        return redirect(url_for("main.interior"))
    return render_template("login.html", form=form)
