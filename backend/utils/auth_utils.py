from functools import wraps

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):

        verify_jwt_in_request()

        claims = get_jwt()

        if claims.get("role") != "admin":
            return jsonify({
                "error": "Admin access required"
            }), 403

        return function(*args, **kwargs)

    return wrapper