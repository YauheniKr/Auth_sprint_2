from functools import wraps

from flask import make_response
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("is_administrator"):
                return fn(*args, **kwargs)
            else:
                return make_response("Admins only!", 403)

        return decorator

    return wrapper
