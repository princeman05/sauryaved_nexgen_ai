
from models import db

class Interview(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(db.Integer)

    category = db.Column(db.String(100))

    score = db.Column(db.Integer)

    feedback = db.Column(db.Text)
