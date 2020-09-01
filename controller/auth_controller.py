from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields
from service.auth_service import Auth
from service.auth_service import authenticated

api = Namespace(name='Auth API', path='/api/auth')

@api.route('/login')
class UserLogin(Resource):
    @api.doc(description='Login user', security='Basic Auth', responses={200: 'Success', 401: 'Not Authorized'})
    #@api.expect(model_login, validate=True)
    def post(self):
        return Auth.login(request)

@api.route('/logout')
class UserLogout(Resource):
    @authenticated
    @api.doc(description='Logout user', security='Bearer Auth')
    def post(current_user,self):
        auth_header = request.headers.get('Authorization')
        return Auth.logout(data=auth_header) 