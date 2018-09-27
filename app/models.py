from app import db

class Satellite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(64))
    port = db.Column(db.Integer)
    name = db.Column(db.String(64))

   