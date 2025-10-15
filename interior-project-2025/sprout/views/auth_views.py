import functools

from flask import Blueprint, request, redirect, url_for, flash, render_template, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from sprout import db
from sprout.forms import UserCreateForm, UserLoginForm
from sprout.models import User

bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        # 사용자명 중복 체크
        existing_username = User.query.filter_by(username=form.username.data).first()
        if existing_username:
            flash('이미 존재하는 사용자입니다.', 'danger')
            return render_template('auth/signup.html', form=form)

        # 이메일 중복 체크
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('이미 등록된 이메일입니다.', 'danger')
            return render_template('auth/signup.html', form=form)

        # 중복이 없으면 회원가입 진행
        try:
            user = User(
                username=form.username.data,
                password=generate_password_hash(form.password1.data),
                email=form.email.data,
                phone=form.phone.data
            )
            db.session.add(user)
            db.session.commit()
            flash('회원가입이 완료되었습니다.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('회원가입 중 오류가 발생했습니다. 다시 시도해주세요.', 'danger')
            print(f"회원가입 오류: {e}")
            return render_template('auth/signup.html', form=form)

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
            _next = request.args.get('next', '')
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('main.index'))
        else:
            flash(errormsg)
    return render_template('auth/login.html', form=form)


# 라우팅 함수보다 먼저 실행하는 함수
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


# 로그아웃
@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


# login_required 데코레이터 함수
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)

    return wrapped_view