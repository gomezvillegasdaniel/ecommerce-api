from flask_jwt import current_identity

from functools import wraps


def is_admin():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if current_identity.role == 'admin':
                return fn(*args, **kwargs)
            else:
                return {
                    'message': 'User has not permission to perform this operation'
                }, 403
        return decorator
    return wrapper
