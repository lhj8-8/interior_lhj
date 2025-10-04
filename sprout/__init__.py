from flask import Flask, g
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SECRET_KEY'] = '4565656246565'

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # 블루프린트 등록
    from .views import main_views, auth_views, product_views, user_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(product_views.bp)
    app.register_blueprint(user_views.bp)

    # DB에서 로그인 사용자 정보 불러오기
    @app.before_request
    def load_logged_in_user():
        from flask import session
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            from .models import User
            g.user = User.query.get(user_id)

    return app