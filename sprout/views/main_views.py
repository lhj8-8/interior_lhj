from flask import Blueprint

bp = Blueprint ('main',__name__)
@bp.route('/')
def index():
    return '새싹팀 파이팅'
