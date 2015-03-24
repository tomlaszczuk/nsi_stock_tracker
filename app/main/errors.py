from flask import render_template
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('_errors/404.html'), 404


@main.app_errorhandler(500)
def server_error(e):
    return render_template('_errors/500.html'), 500


@main.app_errorhandler(403)
def forbidden(e):
    return render_template('_errors/403.html'), 403
