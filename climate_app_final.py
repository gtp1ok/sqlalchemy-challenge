# Import needed libraries

import numpy as np
import datetime as dt
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify
from sqlalchemy import create_engine, func

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model and table
Base = automap_base()
Base.prepare(engine, reflect=True)


# save reference to the table
#station = Base.classes.station
#measurement = Base.classes.measurement
#station = Base.classes.station

#session = Session(engine)


# Flask setup
app = Flask(__name__)

# Creating routes
@app.route("/")
def welcome():
    """List all available api routes."""

    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitations<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# # create precipitation route
# Query precipitation and date values 
# Create a dictionary using date as the key and prcp as the value
@app.route("/api/v1.0/precipitations")
def prcp():
    session = Session(engine)
    measurement = Base.classes.measurement
    date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= date).all()
    #results_prcp = session.query(measurement.date, measurement.prcp).all()
    session.close()

    precipitation = []
    for date, prcp in results:
        precipitation_dict = {date: prcp}
        precipitation.append(precipitation_dict)
   
    return jsonify(precipitation)
   
# Return a JSON list of stations from the dataset
# Create a dictionary to hold station data
@app.route("/api/v1.0/station")
def stationa():
    session = Session(engine)
    station = Base.classes.station
   
    results = session.query(station.name).all()
    results_list = list(np.ravel(results))
    session.close()

    return jsonify(results_list)
 
# Query the dates and temperature observations of the most active station for the previous year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.  

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    measurement = Base.classes.measurement
    #station = Base.classes.station
    
    results = session.query(measurement.tobs).\
            filter(measurement.station == "USC00519281").\
            filter(measurement.date >= "2016-08-23").all()
    session.close()
    
    temps = list(np.ravel(results))
    
    return jsonify(temps)
###################################################################

if __name__ == '__main__':
    app.run(debug=True)