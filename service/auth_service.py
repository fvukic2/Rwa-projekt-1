from flask import request,make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

from model import db
from model.user import User
from model.token_blacklist import TokenBlacklist

from config import secret_key, admin_key

class Auth:

    @staticmethod
    def login(request):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

        user = User.query.filter_by(email=auth.username).first()

        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

        if check_password_hash(user.password, auth.password):
            token = jwt.encode({'email' : user.email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, secret_key)
            blacklist_tokens = TokenBlacklist.query.all()
            if blacklist_tokens == []:
                pass
            else:
                for i in blacklist_tokens:
                    if i.token == token:
                        token = jwt.encode({'email' : user.email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, secret_key)
                    else:
                        pass

            return {'token' : token.decode('UTF-8')}

        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    @staticmethod
    def logout(data):
        token = request.headers['Authorization']
        new_blacklist_token = TokenBlacklist(token=token)
        db.session.add(new_blacklist_token)
        db.session.commit()
        return {}, 200  

# decorator used for guarding api endpoints from public access
def authenticated(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return {'message' : 'Auth token is missing!'}, 401

        try: 
            data = jwt.decode(token, secret_key)
            current_user = User.query.filter_by(email=data['email']).first()
        except:
            return {'message' : 'Auth token is invalid!'}, 401

        print("AUTH OK =>", current_user.email)    

        return f(current_user, *args, **kwargs)

    return decorated

# decorator used for guarding api endpoints from non-admin access
def authenticated_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return {'message' : 'Auth token is missing!'}, 401

        try: 
            data = jwt.decode(token, secret_key)
            current_user = User.query.filter_by(email=data['email']).first()
        except:
            return {'message' : 'Auth token is invalid!'}, 401

        if current_user.admin:
            print("ADMIN AUTH OK =>", current_user.email)    
            return f(current_user, *args, **kwargs)
        else:
            return {'message' : 'Admin permission required!'}, 403

    return decorated    