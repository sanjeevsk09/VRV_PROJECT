from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps



def role_required(required_role):
    def wrapper(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            user_identity = get_jwt_identity()
            if user_identity["role"] != required_role:
                return jsonify({"msg": "Access denied"}), 403
            return func(*args, **kwargs)
        return wrapped_function
    return wrapper