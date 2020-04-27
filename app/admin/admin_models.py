from flask import current_app as app
from .. import db, ma
from ..main.main_models import User

class Admin(User):
    __tablename__ = "covscan19_admins"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column( db.String( 80 ), index = False, \
                        nullable = False
                        )
    admin = db.Column( db.Boolean, index = False, \
                        unique = False, nullable = False
                        )

class AdminSchema(ma.ModelSchema):
    class Meta:
       model = Admin
       fields = ("id", "name", "email", "created")