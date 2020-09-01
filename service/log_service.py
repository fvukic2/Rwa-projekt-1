from flask import request,make_response
import jwt
import datetime
from functools import wraps

# decorator used for tracing API calls
def trace(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        ## TODO Implement custom tracing logic
        ## print(f'{}')
        return f(*args, **kwargs)

    return decorated