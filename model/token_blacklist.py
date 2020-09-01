from . import db

class TokenBlacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Text)