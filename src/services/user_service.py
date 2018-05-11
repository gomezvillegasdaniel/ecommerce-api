from flask_jwt import current_identity

from functools import wraps


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if current_identity.role == 'admin':
                return fn(*args, **kwargs)
            return {
                    'message': 'User has not permission to perform this operation'
                }, 403
        return decorator
    return wrapper
