from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields
from model import db
from model.user import User
from werkzeug.security import generate_password_hash
import datetime
import re

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

def check(email):  
    if(re.search(regex,email)):  
       return True 
    else:  
        return False

api = Namespace(name='First time API', path='/api')

@api.route('/db-init')
class createDbFirstTime(Resource):
    @api.doc(description='First time database initalization', responses={200: 'Success'})
    def post(self):
        db.create_all()
        return {'message': 'Database succesfully initalized'}
    
@api.route('/add-first-admin')
@api.param('email', 'First admin email', type='email')
@api.param('first_name', 'First admin first name')
@api.param('last_name', 'First admin last name')
@api.param('password', 'First admin password')
@api.response(406, 'Invalid email address')
class addFirstAdmin(Resource):
    @api.doc(description='Add first admin', responses={200: 'Success'})
    def post(self):
        if check(request.args.get('email')):
            admin = User(id=1, email=request.args.get('email'), first_name=request.args.get('first_name'), 
            last_name=request.args.get('last_name'), password=generate_password_hash(request.args.get('password')), admin=True)
            db.session.add(admin)
            db.session.commit()
            return {'message': 'First admin succesfuly added'}
        else:
            api.abort(406)