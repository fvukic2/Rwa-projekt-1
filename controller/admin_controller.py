from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from model import db
from model.upit import Upit
from service.auth_service import authenticated, authenticated_admin
from service.log_service import trace

api = Namespace(name='Admin Upit API', path='/api/upit', decorators=[trace])

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


@api.route('/')
class UpitiListResource(Resource):
  
    @api.doc(description='Stvori upit', responses={201: 'Success', 401: 'Unauthorized'}, security='Bearer Auth')
    @api.expect(upit_create)
    @api.marshal_with(upit_dto)
    @authenticated_admin
    def post(current_user,self):
        novi_upit = Upit(naslov=api.payload['naslov'], poruka=api.payload['poruka'], user_id=current_user.id)
        db.session.add(novi_upit)
        db.session.commit()
        
        return novi_upit, 201

    @api.doc(description='Svi upiti', responses={200: 'Success', 403: 'Forbidden'}, security='Bearer Auth')
    @api.marshal_list_with(upit_dto)
    @api.param('naslov', description='Naslov', type='string')
    @api.param('poruka', description='Poruka', type='string')
    @authenticated_admin
    def get(current_user, self):
        
        naslov = request.args.get('naslov')
        poruka = request.args.get('poruka')
        
        upiti = Upit.query.all()

        if naslov:
            upiti = upiti.filter(Upit.naslov.ilike('%'+naslov+'%'))
        if poruka:
            upiti = upiti.filter(Upit.poruka.ilike('%'+poruka+'%'))

        output = []

        for upit in upiti:
            upit_data = {}
            upit_data['id'] = upit.id
            upit_data['naziv'] = upit.naslov
            upit_data['poruka'] = upit.poruka
            upit_data['user_id'] = upit.user_id            
            upit_data['created'] = upit.created
            upit_data['updated'] = upit.updated
            output.append(upit_data)

        return output     

@api.route('/<id>')
@api.param('id', 'ID')
@api.response(404, 'Upit nije pronađen.')
class UpitResource(Resource):
    @api.doc(description='Dohvati upit', responses={200: 'Success', 403: 'Forbidden'}, security='Bearer Auth')
    @api.marshal_with(upit_dto)
    @authenticated_admin
    def get(current_user, self, id):
        upit = Upit.query.filter_by(id=id).first()
        if not upit:
            api.abort(404)
        else:
            return upit  

    @api.doc(description='Ažuriraj upit', responses={200: 'Success', 403: 'Forbidden'}, security='Bearer Auth')
    @api.marshal_with(upit_dto)
    @api.param('naslov', description='Naslov', type='string')
    @api.param('poruka', description='Poruka', type='string')
    @authenticated_admin
    def put(current_user, self, id):
        upit = Upit.query.filter_by(id=id).first()
        if not upit:
            api.abort(404)
        else:
            naslov = request.args.get('naslov')
            poruka = request.args.get('poruka')

            if naslov:
                upit.naslov = naslov

            if poruka:
                upit.poruka = poruka

            db.session.commit()
            return upit            

    @api.doc(description='Izbriši upit', responses={200: 'Success', 403: 'Forbidden'}, security='Bearer Auth')
    @authenticated_admin
    def delete(current_user, self, id):
        upit = Upit.query.filter_by(id=id).first()
        if not upit:
            api.abort(404)
        else:
            db.session.delete(upit)
            db.session.commit()
            return {'message':'Upit je izbrisan!'}         