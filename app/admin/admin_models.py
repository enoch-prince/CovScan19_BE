from flask import current_app as app
from .. import db
from ..main.main_models import User

class Admin(User):
    __tablename__ = "covscan19_admins"
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column( db.Boolean, index = False, \
                        unique = False, nullable = False
                        )