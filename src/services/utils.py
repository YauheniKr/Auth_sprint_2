from functools import wraps

from flask import make_response
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_restful import abort


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


def get_paginated_list(results, url, page, limit):
    page = int(page)
    limit = int(limit)
    count = len(results)
    if count < page or limit < 0:
        abort(404)
    # make response
    obj = {}
    obj['page'] = page
    obj['limit'] = limit
    obj['count'] = count
    # make URLs
    # make previous url
    if page == 1:
        obj['previous'] = ""
    else:
        obj['previous'] = f'{url}?page={page-1}&limit={limit}'
    # make next url
    if page * limit > count:
        obj['next'] = ""
    else:
        obj['next'] = f'{url}?page={page+1}&limit={limit}'
    # finally extract result according to bounds
    obj['results'] = results[limit*(page - 1):page * limit]
    return obj
