from . import db

class Upit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naslov = db.Column(db.String(50))
    poruka = db.Column(db.String(50))
    user_id = db.Column(db.String(50))
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())