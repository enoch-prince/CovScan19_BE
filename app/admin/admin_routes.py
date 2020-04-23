from flask import current_app as app
from .admin_models import Admin
from ..main.main_models import Patient

@app.route("/admin")
def adminIndex():
    return { "msg": "The Admin Homepage" }

@app.route("/admin/api/admin")
def getAdmin():
    res = Admin.query.all()
    return { "data": res }

@app.route("/admin/api/patient")
def getPatient():
    res = Patient.query.all()
    return { "data": res }