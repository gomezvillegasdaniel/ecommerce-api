from flask_jwt import current_identity

from models.purchase_log_model import PurchaseLogModel

from functools import wraps


def log_purchase():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            fn_response = fn(*args, **kwargs)
            if fn_response.get('successful_purchase'):
                log = PurchaseLogModel(current_identity, *args)
                log.save_to_db()
            return fn_response
        return decorator
    return wrapper
