from flask import Blueprint, redirect

general_bp = Blueprint("general", __name__)


@general_bp.route("/")
def index():
    return redirect("/apidocs")
