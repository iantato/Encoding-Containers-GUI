from flask import render_template

from app.home.base import home_bp

@home_bp.route("/", methods=["GET"])
def index_route():
    return render_template("home.html")