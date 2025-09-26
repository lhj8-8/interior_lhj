from flask import Blueprint, render_template

bp = Blueprint ('main',__name__)
@bp.route('/')
def index():
    return render_template('main.html')

@bp.route("/sub")
def sub_page():
    return render_template("sub.html")
