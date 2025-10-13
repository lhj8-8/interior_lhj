<<<<<<< HEAD
<<<<<<< HEAD
from flask import Flask, g, session
=======
from flask import Flask
>>>>>>> upstream/main
=======
from flask import Flask, g, session
>>>>>>> upstream/develop
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SECRET_KEY'] = '4565656246565'

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> upstream/develop
    # 세션 쿠키 설정 추가 (중요!)
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1시간

<<<<<<< HEAD
=======
>>>>>>> upstream/main
=======
>>>>>>> upstream/develop
    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> upstream/develop
    # 블루프린트 등록
    from .views import main_views, auth_views, product_views, user_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(product_views.bp)
    app.register_blueprint(user_views.bp)

    # DB에서 로그인 사용자 정보 불러오기
    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            from .models import User
            g.user = User.query.get(user_id)
            if g.user:
                print(f"✓ 사용자 로드됨: {g.user.username} (ID: {g.user.id})")
            else:
                print(f"⚠ User ID {user_id}를 찾을 수 없음")

<<<<<<< HEAD
    return app
=======
    # 블루 프린트 등록
    from .views import main_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)

    return app
>>>>>>> upstream/main
=======
    return app
>>>>>>> upstream/develop
