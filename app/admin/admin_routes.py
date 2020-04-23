from flask import current_app as app
from .admin_models import Admin, AdminSchema
from ..main.main_models import Patient

admin_schema = AdminSchema()

@app.route("/admin")
def adminIndex():
    return { "msg": "The Admin Homepage" }

@app.route("/admin/api/admin")
def getAdmin():
    all_admins = Admin.query.all()
    output = admin_schema.dumps(all_admins).data
    return { "data": output }

@app.route("/admin/api/patient")
def getPatient():
    res = Patient.query.all()
    return { "data": res }