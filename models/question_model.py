from models import db

class Question(db.Model):

    id = db.Column(

        db.Integer,

        primary_key=True
    )

    category = db.Column(

        db.String(100)
    )

    difficulty = db.Column(

        db.String(50)
    )

    question = db.Column(

        db.Text
    )