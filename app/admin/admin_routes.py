from flask import request, url_for, redirect, render_template, flash
from flask import current_app as app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime as dt
from datetime import timedelta
from .. import db
from ..util import find_user, find_by_id
from .admin_models import *
from ..main.main_models import *

admin_schema = AdminSchema()
login_manager.login_view = 'login'

### Some Functions ###
def getRecentMonitored(days):
    items = []
    patients = []
    threshold = dt.now() - timedelta(days=days)
    results = VitalStatistics.query.filter(VitalStatistics.timestamp > threshold).all()
    for result in results:
        if len(items) >= 0:
            for i in items:
                if result.history.patient_id == i["ID"]:
                    if result.timestamp > i["Timestamp"]:
                        i["Timestamp"] = result.timestamp
                        break
            else:
                items.append(
                    {
                        "ID": result.history.patient_id,
                        "Name": result.history.patient.name,
                        "Timestamp": result.timestamp
                    }
                )
    return items

def getTotalStats():
    t_patients = Patient.query.all()
    t_history = [hist for patient in t_patients for hist in patient.history]
    t_vstats = [vstat for hist in t_history for vstat in hist.vital_stats]
    return len(t_patients), len(t_vstats)


# @app.route("/admin")
# def adminIndex():
#     return render_template('index.html')

@app.route("/admin", methods=["GET", "POST"])
@app.route("/admin/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        user = Admin.query.filter_by(name=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
    
        error = 'Invalid username or password'
        #return redirect( url_for("login") )
    
    return render_template('login.html', form = form, error = error)

@app.route("/admin/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = Admin( name=form.username.data, dob=form.dob.data, email=form.email.data, \
                         password=hashed_password, created=dt.now() )
        db.session.add(new_user)
        db.session.commit()
        msg = f"{new_user.name} is now an Admin!"

        return redirect( url_for("getAllAdmins", msg=msg) )
    
    return render_template('signup.html', form = form)

@app.route('/admin/dashboard')
@login_required
def dashboard():
    recent_monitored = getRecentMonitored(5)
    stats = getTotalStats()
    return render_template('dashboard.html', name=current_user.name, \
                            recent=recent_monitored, vstats=stats[1], \
                            patients=stats[0])

@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



#### Api's with respect to the Admin Model ####
@app.route("/admin/dashboard/admins")
@login_required
def getAllAdmins():
    msg = None
    if request.args:
        msg = request.args.get("msg")
    all_admins = Admin.query.all()
    admin_schema.many = True
    results = admin_schema.dump(all_admins)
    return render_template("display_admins.html", admins=results, msg=msg)

@app.route("/admin/api/admin/<name_or_id>")
def getAdmin(name_or_id):
    if name_or_id.isdigit():
        admin = Admin.query.get_or_404(int(name_or_id), description=f"ID {name_or_id} not found!")
        admin_schema.many = False
        return admin_schema.dumps(admin)
    
    admin = Admin.query.filter(name=name_or_id).first_or_404(description=f"{name_or_id} not found")
    return admin_schema.dumps(admin)

@app.route("/admin/api/admin", methods=["POST", "PUT", "DELETE"])
def adminUser():
    if request.method == "POST":
        credentials = find_user(request, Admin)
        if isinstance(credentials, tuple):# if returns (userdata, modelObject)
            return { "msg": f"{credentials[0]['name']} already exits in database!" }
        if isinstance(credentials, int):# if returns 13
            return {"msg": "Please enter at least name and dob"}
        
        # esle credentials is instance of dict
        new_admin = Admin( name=credentials["name"], email=credentials["email"], \
                            dob=credentials["dob"], created=dt.now(), \
                            password=credentials["password"] 
                        )
        db.session.add( new_admin )
        db.session.commit()
        return redirect(url_for("getAllAdmins"))
    
    if request.method == "PUT": 
        admin_data = request.json
        admin_obj = find_by_id(admin_data.get("id"), Admin)
        for key, value in admin_data.items():
            setattr(admin_obj, key, value)
        db.session.commit()
        # return admin_schema.dumps(admin_obj)
        return redirect( url_for("getAdmin", name_or_id=f"{admin_obj.id}") )         
    
    if request.method == "DELETE":
        admin_obj = find_by_id(request.json.get("id"), Admin)
        db.session.delete( admin_obj )
        db.session.commit()
        # return redirect(url_for("getAllAdmins", msg=f"{admin_obj.name} deleted successfully!"))
        return { "msg": f"{admin_obj.name} deleted successfully!" }




# #### All api's with respect to the Patient Model ####
# patient_schema = PatientSchema()

# @app.route("/admin/api/patient")
# def getAllPatients():
#     all_patients = Patient.query.all()
#     patient_schema.many = True
#     return {"msg": "No Patients registered!"} if len(all_patients) == 0 else { "data": patient_schema.dump(all_patients) }

# @app.route("/admin/api/admin/<name_or_id>")
# def getPatient(name_or_id):
#     if name_or_id.isdigit():
#         patient = Patient.query.get_or_404(int(name_or_id), description=f"ID {name_or_id} not found!")
#         patient_schema.many = False
#         return patient_schema.dumps(patient)
    
#     patient = Patient.query.filter(name=name_or_id).first_or_404(description=f"{name_or_id} not found")
#     return patient_schema.dumps(patient)


# @app.route("/admin/api/patient", methods=["POST", "PUT", "DELETE"])
# def editPatient():
#     credentials = find_user(request, Patient)

#     if request.method == "POST":
#         if isinstance(credentials, tuple):# if returns (userdata, modelObject)
#             return { "msg": f"{credentials[0]['name']} already exits in database!" }
#         if isinstance(credentials, int):# if returns 13
#             return {"msg": "Please enter at least name and email"}
        
#         # esle credentials is instance of dict
#         new_patient = Patient( name=credentials["name"], email=credentials["email"], \
#                             tel=credentials["tel"] or "", created=dt.now(), bio=credentials["bio"], \
#                             location=credentials["location"] or "", status=credentials["status"] or "" )
#         db.session.add( new_patient )
#         db.session.commit()

#         return redirect(url_for("getAllPatients"))
    
#     if request.method == "PUT":
#         if isinstance(credentials, tuple):
#             # then user exisits
#             patient_data, patient_obj  = credentials
#             for key, value in patient_data.items():
#                 setattr(patient_obj, key, value)
#             db.session.commit()
#             return redirect( url_for("getPatient", name_or_id=f"{patient_obj.id}") )         
    
#     if request.method == "DELETE":
#         if isinstance(credentials, tuple):
#             patient_schema.many = True
#             patient_obj  = credentials[1]
#             db.session.delete( patient_obj )
#             db.session.commit()
#             return redirect(url_for("getAllPatients"))
#         return {"msg": "Delete request failed flawlessly!"}