from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from model import db
from model.user import User
from service.auth_service import authenticated, authenticated_admin
import re

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

def check(email):  
    if(re.search(regex,email)):  
       return True 
    else:  
        return False

api = Namespace(name='Manage Users API', path='/api/users')

user_dto = api.model('User', {
    'email': fields.String(required=True, description='Email'),
    'first_name': fields.String(required=True, description='First Name'),
    'last_name': fields.String(required=True, description='Last Name'),
    'password': fields.String(required=True, description='Password'),
    'admin': fields.Boolean(required=True, description='Admin'),
    'created': fields.DateTime(required=True, description='Created'),
    'updated': fields.DateTime(required=True, description='Updated')
})

user_signup_dto = api.model('UserSignup', {
    'email': fields.String(required=True, description='Email'),
    'first_name': fields.String(required=True, description='First Name'),
    'last_name': fields.String(required=True, description='Last Name'),
    'password': fields.String(required=True, description='Password')
})

user_update_dto = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='First Name'),
    'last_name': fields.String(required=False, description='Last Name')
})

@api.route('/')
class UserListResource(Resource):
    @api.doc(description='Signup', responses={201: 'Success', 406: 'Ivalid email address'})
    @api.expect(user_signup_dto)
    def post(self):
        if check(api.payload['email']):
            hashed_password = generate_password_hash(api.payload['password'], method='sha256')
            new_user = User(email=api.payload['email'], first_name=api.payload['first_name'], last_name=api.payload['last_name'], password=hashed_password, admin=False)
            db.session.add(new_user)
            db.session.commit()
        
            return {'message': 'New user created!'}, 201
        else:
            api.abort(406)

    @api.doc(description='Get all user details', responses={200: 'Success', 401: 'Unauthorized'}, security='Bearer Auth')
    @api.marshal_with(user_dto)
    @authenticated_admin
    def get(current_user, self):
        users = User.query.all()

        return users      


    @api.doc(description='Update user details', responses={200: 'Success', 401: 'Unauthorized'}, security='Bearer Auth')
    @api.expect(user_update_dto)
    @authenticated
    def put(current_user, self):
        if 'first_name' in api.payload:
            current_user.first_name = api.payload['first_name']

        if 'last_name' in api.payload:
            current_user.last_name = api.payload['last_name']    

        db.session.commit()        
        
        return {'message': 'User updated!'}, 200   


@api.route('/<email>')
@api.param('email', 'User email address')
@api.response(404, 'User not found.')
class UserResource(Resource):
    @api.doc(description='Get a user', responses={200: 'Success', 403: 'Forbidden'}, security='Bearer Auth')
    @api.marshal_with(user_dto)
    @authenticated_admin
    def get(current_user, self, email):
        user = User.query.filter_by(email=email).first()
        if not user:
            api.abort(404)
        else:
            return user         