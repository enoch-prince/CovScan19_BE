from flask import current_app as app
from .. import db


class User(db.Model):
    __abstract__ = True
    username = db.Column( db.String( 60 ), index=False, \
                        unique = True, nullable = False
                        )
    email = db.Column( db.String( 80 ), index = False, \
                        nullable = False
                        )
    tel = db.Column( db.String( 25 ), index = False, \
                        nullable = False
                        )
    created = db.Column( db.DateTime, index = False, \
                        unique = False, nullable = False
                        )
    bio = db.Column( db.Text, index = False, unique = False, \
                    nullable = True
                    )
    
    def __repr__(self):
        return "<User {}>".format(self.username)




class Patient(User):
    __tablename__ = "covscan19_patients"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column( db.String( 80 ), index = False, \
                        nullable = False
                        )
    status = db.Column( db.String( 80 ), index = False, \
                        nullable = False
                        ) # corona free or not