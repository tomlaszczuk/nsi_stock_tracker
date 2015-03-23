from functools import wraps
from flask import abort
from flask.ext.login import current_user


def admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorator
