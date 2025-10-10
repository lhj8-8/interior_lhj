import functools

from flask import Blueprint, request, redirect, url_for, flash, render_template, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from sprout import db
from sprout.forms import UserCreateForm, UserLoginForm
from sprout.models import User

bp=Blueprint('auth', __name__, url_prefix='/')

@bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.username.data,
                        phone=form.phone.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        errormsg = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            errormsg = '존재하지 않는 사용자입니다.'
        elif not check_password_hash(user.password, form.password.data):
            errormsg = '비밀번호가 올바르지 않습니다.'
        if errormsg is None:
            session.clear()
            session['user_id'] = user.id
            _next = request.args.get('next', '')  # next 파라미터 전달
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('main.index'))
        else:
            flash(errormsg)
    return render_template('auth/login.html',form=form)

#라우팅 함수보다 먼저 실행하는 함수(요청 처리 들어오기 전에 먼저 실행)
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user=User.query.get(user_id)  #g: 플라스크의 컨텍스트 변수. 요청->응답 과정에서 유효

#로그아웃
@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

#login_required 데코레이터 함수 (데코레이트: 반복될 때 활용)
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view