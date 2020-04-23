from flask import current_app as app
from .main_models import Patient

@app.route("/")
def mainIndex():
    return { "msg": "The Main Homepage" }