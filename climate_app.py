import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
# Create a homepage to list all available routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
# Create the precipitation webpage
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of measurement data including the date and prcp"""
    # Query all measurement data
    precipitation_results = session.query(Measurement.date,Measurement.prcp).all()
    # Create a dictionary from the row data and append to a list of all_measurement
    precipitation_by_date = []
    for measurement in precipitation_results:
        precipitation_dict = {}
        precipitation_dict["date"] = measurement.date
        precipitation_dict["prcp"] = measurement.prcp
        precipitation_by_date.append(precipitation_dict)
    return jsonify(precipitation_by_date)
# Create the station webpage
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of station data """
    # Query all stations
    station_results = session.query(Station.station).all()
    # Convert list of tuples into normal list
    station_list = list(np.ravel(station_results))
    return jsonify(station_list)

if __name__ == '__main__':
    app.run(debug=True)

