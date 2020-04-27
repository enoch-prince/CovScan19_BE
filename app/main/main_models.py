from flask import current_app as app
from .. import db, ma

### Base Model Class ###
class User(db.Model):
    __abstract__ = True
    name = db.Column( db.String( 50 ), index=False, \
                        unique = False, nullable = False
                        )
    dob = db.Column( db.String( 25 ), index = False, \
                        unique = False, nullable = True
                        )
    created = db.Column( db.DateTime, index = False, \
                        unique = False, nullable = False
                        )
    # bio = db.Column( db.Text, index = False, unique = False, \
    #                 nullable = True
    #                 )
    
    def __repr__(self):
        return "<User {}>".format(self.name)


### Main Model Classes ###
class Patient(User):
    __tablename__ = "covscan19_patients"
    id = db.Column(db.Integer, primary_key=True)

    hometown = db.Column( db.String( 50 ), index = False, \
                        nullable = True
                        )
    country = db.Column( db.String( 25 ), index = False, \
                        nullable = True
                        )
    height = db.Column( db.Float, index = False, \
                        nullable = True
                        )
    weight = db.Column( db.Float, index = False, \
                        nullable = True
                        )
    history = db.relationship( "History", backref=db.backref( "patient", lazy = "joined" ) )
    


class VitalStatistics(db.Model):
    __tablename__ = "vital_statistics"
    id = db.Column( db.Integer, primary_key = True )
    ambient_temp = db.Column( db.Float, index = False, \
                              unique = False, nullable = False )
    ambient_humidity = db.Column( db.Float, index = False, \
                                    unique = False, nullable = False )
    dist_of_separation = db.Column( db.Float, index = False, \
                                    unique = False, nullable = False )
    temp_burst = db.Column( db.TEXT, index = False, \
                            unique = False, nullable = False )
    history_id = db.Column( db.Integer, db.ForeignKey( "history.id" ) ) #FK=history is the history table inside the database


class History( db.Model ):
    id = db.Column( db.Integer, primary_key = True )
    timestamp = db.Column( db.DateTime, index = False, \
                            unique = False, nullable = False
                        )
    record_mode = db.Column( db.String( 25 ), index = False, \
                             nullable = True
                            )
    patient_id = db.Column( db.Integer, db.ForeignKey( "covscan19_patients.id" ) )
    vital_stats = db.relationship( "VitalStatistics", backref = db.backref( "history", lazy = "joined" ) ) # backref=history creates a column called history in VitalStatistics table



### Schema Classes ###
class PatientSchema( ma.ModelSchema ):
    class Meta:
       model = Patient
       fields = ("id", "name", "dob", "hometown", "country", "created")


class VitalStatsSchema( ma.ModelSchema ):
    class Meta:
        model = VitalStatistics
        fields = ("id", "ambient_temp", "ambient_humidity", "dist_of_separation", "temp_burst")


class HistorySchema( ma.ModelSchema ):
    class Meta:
        model = History
        fields = ("id", "timestamp", "record_mode")