from flask import request, url_for, redirect
from flask import current_app as app
from datetime import datetime as dt
from .. import db
from .admin_models import Admin, AdminSchema
from ..util import find_user
from ..main.main_models import Patient, PatientSchema

admin_schema = AdminSchema()

@app.route("/admin")
def adminIndex():
    return { "msg": "The Admin Homepage" }

#### Api's with respect to the Admin Model ####
@app.route("/admin/api/admin")
def getAllAdmins():
    all_admins = Admin.query.all()
    admin_schema.many = True
    return {"msg": "No admins registered!"} if len(all_admins) == 0 else { "data": admin_schema.dump(all_admins) }

@app.route("/admin/api/admin/<name_or_id>")
def getAdmin(name_or_id):
    if name_or_id.isdigit():
        admin = Admin.query.get_or_404(int(name_or_id), description=f"ID {name_or_id} not found!")
        admin_schema.many = False
        return admin_schema.dumps(admin)
    
    admin = Admin.query.filter(username=name_or_id).first_or_404(description=f"{name_or_id} not found")
    return admin_schema.dumps(admin)

@app.route("/admin/api/admin", methods=["POST", "PUT", "DELETE"])
def adminUser():
    credentials = find_user(request, Admin)

    if request.method == "POST":
        if isinstance(credentials, tuple):# if returns (userdata, modelObject)
            return { "msg": f"{credentials[0]['username']} already exits in database!" }
        if isinstance(credentials, int):# if returns 13
            return {"msg": "Please enter at least username and email"}
        
        # esle credentials is instance of dict
        new_admin = Admin( username=credentials["username"], email=credentials["email"], \
                            tel=credentials["tel"] or "", created=dt.now(), bio=credentials["bio"], \
                            admin=True )
        db.session.add( new_admin )
        db.session.commit()
        return redirect(url_for("getAllAdmins"))
    
    if request.method == "PUT":
        if isinstance(credentials, tuple):
            # then user exisits
            admin_data, admin_obj  = credentials
            for key, value in admin_data.items():
                setattr(admin_obj, key, value)
            db.session.commit()
            # return admin_schema.dumps(admin_obj)
            return redirect( url_for("getAdmin", name_or_id=f"{admin_obj.id}") )         
    
    if request.method == "DELETE":
        if isinstance(credentials, tuple):
            admin_schema.many = True
            admin_obj  = credentials[1]
            db.session.delete( admin_obj )
            db.session.commit()
            return redirect(url_for("getAllAdmins"))
        return {"msg": "Delete request failed flawlessly!"}




#### All api's with respect to the Patient Model ####
patient_schema = PatientSchema()

@app.route("/admin/api/patient")
def getAllPatients():
    all_patients = Patient.query.all()
    patient_schema.many = True
    return {"msg": "No Patients registered!"} if len(all_patients) == 0 else { "data": patient_schema.dump(all_patients) }

@app.route("/admin/api/admin/<name_or_id>")
def getPatient(name_or_id):
    if name_or_id.isdigit():
        patient = Patient.query.get_or_404(int(name_or_id), description=f"ID {name_or_id} not found!")
        patient_schema.many = False
        return patient_schema.dumps(patient)
    
    patient = Patient.query.filter(username=name_or_id).first_or_404(description=f"{name_or_id} not found")
    return patient_schema.dumps(patient)


@app.route("/admin/api/patient", methods=["POST", "PUT", "DELETE"])
def editPatient():
    credentials = find_user(request, Patient)

    if request.method == "POST":
        if isinstance(credentials, tuple):# if returns (userdata, modelObject)
            return { "msg": f"{credentials[0]['username']} already exits in database!" }
        if isinstance(credentials, int):# if returns 13
            return {"msg": "Please enter at least username and email"}
        
        # esle credentials is instance of dict
        new_patient = Patient( username=credentials["username"], email=credentials["email"], \
                            tel=credentials["tel"] or "", created=dt.now(), bio=credentials["bio"], \
                            location=credentials["location"] or "", status=credentials["status"] or "" )
        db.session.add( new_patient )
        db.session.commit()

        return redirect(url_for("getAllPatients"))
    
    if request.method == "PUT":
        if isinstance(credentials, tuple):
            # then user exisits
            patient_data, patient_obj  = credentials
            for key, value in patient_data.items():
                setattr(patient_obj, key, value)
            db.session.commit()
            return redirect( url_for("getPatient", name_or_id=f"{patient_obj.id}") )         
    
    if request.method == "DELETE":
        if isinstance(credentials, tuple):
            patient_schema.many = True
            patient_obj  = credentials[1]
            db.session.delete( patient_obj )
            db.session.commit()
            return redirect(url_for("getAllPatients"))
        return {"msg": "Delete request failed flawlessly!"}