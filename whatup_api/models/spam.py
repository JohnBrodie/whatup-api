from whatup_api.models import db


class Spam(db.Model):
    __tablename__ = 'spams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))


