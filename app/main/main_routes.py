from flask import current_app as app
from flask import request, url_for, redirect
from datetime import datetime as dt
from .. import db
from .main_models import Patient, PatientSchema
from ..util import find_user, find_by_id


@app.route("/")
def mainIndex():
    return { "msg": "The Main Homepage" }


#### All api's with respect to the Patient Model ####
patient_schema = PatientSchema()

@app.route("/api/patients")
def getAllPatients():
    all_patients = Patient.query.all()
    patient_schema.many = True
    return {"msg": "No Patients registered!"} if len(all_patients) == 0 else { "data": patient_schema.dump(all_patients) }

@app.route("/api/patient/<name_or_id>")
def getPatient(name_or_id):
    if name_or_id.isdigit():
        patient = Patient.query.get_or_404(int(name_or_id), description=f"ID {name_or_id} not found!")
        patient_schema.many = False
        return patient_schema.dumps(patient)
    
    patient = Patient.query.filter(name=name_or_id).first_or_404(description=f"{name_or_id} not found")
    return patient_schema.dumps(patient)


@app.route("/api/patient", methods=["POST", "PUT", "DELETE"])
def editPatient():
    
    if request.method == "POST":
        credentials = find_user(request, Patient)
        if isinstance(credentials, tuple):# if returns (userdata, modelObject)
            return { "msg": f"{credentials[0]['name']} already exits in database!" }
        if isinstance(credentials, int):# if returns 13
            return {"msg": "Please enter at least name and dob"}
        
        # esle credentials is instance of dict
        new_patient = Patient( name=credentials["name"], dob=credentials["dob"], \
                               hometown=credentials["hometown"] or "", created=dt.now(), \
                               height=credentials["height"], weight=credentials["weight"], \
                               country=credentials["country"] or ""
                            )
        db.session.add( new_patient )
        db.session.commit()

        return redirect(url_for("getAllPatients"))
    
    if request.method == "PUT":
        patient_data = request.json
        patient_obj = find_by_id(patient_data.get("id"), Patient)
        for key, value in patient_data.items():
            setattr(patient_obj, key, value)
        db.session.commit()
        return redirect( url_for("getPatient", name_or_id=f"{patient_obj.id}") )         
    
    if request.method == "DELETE":
        patient_obj  = find_by_id(request.json.get("id"), Patient)
        db.session.delete( patient_obj )
        db.session.commit()
        return redirect(url_for("getAllPatients"))

@app.route("/api/patient_data", methods = ["POST", "PUT", "DELETE"])
def patientData():
    if request.method == "POST":
        data = request.json
        patient_obj = find_by_id(data["id"], Patient)
        
    
    if request.method == "PUT":
        pass

    if request.method == "DELETE":
        pass