from whatup_api.models import db

class Egg(db.Model):
    __tablename__ = 'eggs'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
