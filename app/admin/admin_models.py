from flask import current_app as app
from flask_login import UserMixin
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from .. import db, ma, login_manager
from ..main.main_models import User

class Admin(UserMixin, User):
    __tablename__ = "covscan19_admins"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column( db.String( 80 ), index = False, \
                        nullable = False
                        )
    password = db.Column(db.String(80))

class AdminSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
       model = Admin
       ordered = True
       fields = ("id", "name", "email", "created")


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    dob = StringField('date of birth', validators=[InputRequired(), Length(min=8)])
    username = StringField('name', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])