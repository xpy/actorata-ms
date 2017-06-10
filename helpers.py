from flask import make_response, json
from functools import wraps


def json_response(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        res = f(*args, **kwargs)
        response = make_response(json.dumps(res, sort_keys=True, indent=4))
        response.headers['Content-type'] = "application/json"
        return response

    return wrapper
