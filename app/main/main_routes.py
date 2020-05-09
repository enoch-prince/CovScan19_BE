from flask import current_app as app
from flask import request, url_for, redirect
from datetime import datetime as dt
from .. import db
from .main_models import *
from ..util import find_user, find_by_id


@app.route("/")
def mainIndex():
    return { "msg": "The Main Homepage" }


#### All api's with respect to the Patient Model ####
patient_schema = PatientSchema()
vs_schema = VitalStatsSchema(many=True)
history_schema = HistorySchema(many=True)

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
    
    patient = Patient.query.filter(Patient.name.contains(name_or_id)).all()
    patient_schema.many = True
    return { "msg": f"{name_or_id} not found!"} if len(patient) == 0 else { "data": patient_schema.dump(patient) }


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
        patient_history = History( date = dt.now().strftime("%a, %d %B, %Y"), \
                                    patient = new_patient 
                                )
        db.session.add( new_patient )
        db.session.add( patient_history )
        db.session.commit()

        return redirect( url_for("getAllPatients") )
    
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
        return redirect( url_for("getAllPatients") )

@app.route("/api/vitalstatistics")
def getAllVitalStats():
    v_stats = VitalStatistics.query.all()
    return { "data": vs_schema.dump( v_stats ) }


@app.route("/api/patient/<id>/vitalstats")
def getVitalStats(id):
    # Gets all the vital stats of patient by id
    patient = find_by_id(id, Patient)
    data = None
    for history in patient.history:
        data = [v_stats for v_stats in history.vital_stats]
    return { "name": patient.name, "id": patient.id, "data": vs_schema.dump( data ) }



@app.route("/api/patient/<id>/vitalstats", methods = ["PUT", "DELETE"])
def editVitalStats(id):
    patient = find_by_id(id, Patient)
    data = request.json
    found = []
    for history in patient.history:
        found = [True for v_stat in history.vital_stats if data["id"] == v_stat.id]
    
    if len(found) == 0:
        return { "msg": "Couldn't find the patient data specified!" }
    
    if request.method == "DELETE":
        v_stat = find_by_id( data["id"], VitalStatistics )
        db.session.delete( v_stat )
        db.session.commit()
        return redirect( url_for("getVitalStats", id = id) )
    
    if request.method == "PUT":
        vs_id = data.get("id")
        v_stat = find_by_id(vs_id, VitalStatistics)
        for key, value in data.items():
            setattr(v_stat, key, value)
        
        db.session.commit()
        
        return redirect( url_for("getVitalStats", id = id) )



@app.route("/api/patient_data", methods = ["POST", "PUT", "DELETE"])
def patientData():
    if request.method == "POST":
        data = request.json
        patient_obj = find_by_id( data["id"], Patient )
        # check for the date of post
        current_date = dt.now().strftime("%a, %d %B, %Y")
        history = None
        
        for hist in patient_obj.history:
            history = hist if current_date == hist.date else history
        if history is None:
            # create new history
            history = History( date = current_date, \
                                    patient = patient_obj 
                                )
            # add to database
            db.session.add( history )
            db.session.commit()
        
        # create patient data in database
        v_stats = VitalStatistics( ambient_temp = data["ambientTemperature"], \
                                   ambient_humidity = data["ambientHumidity"], \
                                   dist_of_separation = data["distanceOfSeparation"], \
                                   temp_burst = data["temperatureBurst"], \
                                   record_mode = data["recordMode"], history = history,
                                   timestamp = dt.now()
                                 )
        db.session.add( v_stats )
        db.session.commit()
        return redirect( url_for("getVitalStats", id = patient_obj.id) )
    
    if request.method == "PUT":
        return { "msg": "Endpoint Not Implemented!" }

    if request.method == "DELETE":
        # Deletes all vital stats and history
        patient = find_by_id(request.json.get("id"), Patient)
        for history in patient.history:
            for v_stats in history.vital_stats:
                db.session.delete( v_stats )
            db.session.delete( history )
        db.session.commit()
        return redirect( url_for("getVitalStats", id = patient.id) )



@app.route("/api/allhistory")
def getAllHistory():
    histories = History.query.all()
    return { "data": history_schema.dump(histories) }


@app.route("/api/patient/<id>/history")
def getPatientHistory(id):
    patient = find_by_id( id, Patient )
    return { "name": patient.name, "id": patient.id, "data": history_schema.dump(patient.history) }


@app.route("/api/patient/<id>/history/<hid>")
def getPatientSpecificHistory(id, hid):
    patient = find_by_id( id, Patient )
    data = [hist for hist in patient.history if int(hid) == hist.id]
    print("<---Data--->:", len(data))
    return { "name": patient.name, "id": patient.id, "data": history_schema.dump( data ) }
