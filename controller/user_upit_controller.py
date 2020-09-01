from flask import request, jsonify
from flask.globals import current_app
from flask_restplus import Namespace, Resource, fields
from model import db
from model.upit import Upit
from werkzeug.security import generate_password_hash
import datetime
from service.auth_service import authenticated

api = Namespace(name='User API', path='/api')

upit_create = api.model('NapraviUpit', {
    'naslov': fields.String(required=True, description='Naslov'),
    'poruka': fields.String(required=True, description='Poruka')
})

upit_dto = api.model('Upit', {
    'id': fields.Integer(required=True, description='ID'),
    'naslov': fields.String(required=True, description='Naslov'),
    'poruka': fields.String(required=True, description='Poruka'),
    'user_id': fields.Integer(required=True, description='User ID'),
    'created': fields.DateTime(required=True, description='Created'),
    'updated': fields.DateTime(required=True, description='Updated')
})


@api.route('/upiti')
class Upiti(Resource):
    @api.doc(description='Svi moji upiti', responses={200: 'Success', 401: 'Unauthorized'}, security='Bearer Auth')
    @authenticated
    def get(current_user, self):
        upiti = Upit.query.filter_by(user_id=current_user.id)
        if upiti == []:
            return "Nema upita u bazi podataka"
        else:
            output = []
            for upit in upiti:
                upit_data = {}
                upit_data['id'] = upit.id
                upit_data['naslov'] = upit.naslov
                upit_data['poruka'] = upit.poruka
                output.append(upit_data)
            return output

    @api.doc(description='Stvori upit', responses={200: 'Success', 401: 'Unauthorized'}, security='Bearer Auth')
    @api.expect(upit_create)
    @api.marshal_with(upit_dto)
    @authenticated
    def post(current_user, self):
        novi_upit = Upit(naslov=api.payload['naslov'], poruka=api.payload['poruka'], user_id=current_user.id)

        db.session.add(novi_upit)
        db.session.commit()
        
        return novi_upit, 201