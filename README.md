### Configuring MySQL Connector for Flask 

Run the following code from the command line *Ubuntu Users*
```bash

sudo apt-get install python3.7-dev libmysqlclient-dev

```

This is *specific for python 3.7*. Just replace the python version with what you have installed

### Install Python Dependencies

```bash

pip install -r requirements.txt

```

### List of Api Endpoints
* **/api/patients** - A GET request that retrieves all registered patients from the database.
* **/api/patient/<name_or_id>** - A GET request that retrieves a specific patient's details either by name or id.
* **/api/patient** - A POST, PUT or DELETE request with request body being json:
     > ```python
     >           { 
     >              "name": "Davi Elikplim",
     >              "dob": "01.12.2000",
     >              "hometown": "Sorgakorpe",
     >              "country": "Ghana",
     >              "height": 5.5,
     >              "weight": 66.7
     >            }
     > ```

    *PUT* and *DELETE* requests only require the ID of the Patient in the request body

* **/api/patient/<id>/vitalstats** - A GET request that retrieves the vital statistics data of a patient specified by an id.
* **/api/patient/<id>/vitalstats** - A DELETE request of a patient's specific vital stats specified by an id by json.
    > An example:
    >
    > Patient with ID 2 - /api/patient/2/vitalstats
    >
    > Body of request will be: ```python { id: 5 } ```
    >
    > This implies a request to delete the vitalstats of ID 5 of Patient with ID 2
* **/api/patient_data** - A POST or DELETE request:
    **POST request** - creates the vital statistics data of patient (using the pateint's id)as well as a history of all created data. The request body will be:
    
    > ```python
    >           { 
    >              "id": 2,
    >              "ambientTemperature": 30,
    >              "ambientHumidity": 15.0,
    >              "distanceOfSeparation": 5.5,
    >              "recordMode": "continuous",
    >              "temperatureBurst": "[12.3, 23.56, 45.32,...]"
    >            }
    > ```

    **DELETE request** - Deletes all vital stats data including the history from the database. Requires only the *id* of patient in the *request body*.
* **/api/allhistory** - A GET request for all vital stats history of all patients ever recorded.
* **/api/patient/<id>/history** - GET request for all vital stats history for the specified patient by id.
* **/api/patient/<id>/history/<hid>** - GET request of a specific patient (id) specific history (hid)