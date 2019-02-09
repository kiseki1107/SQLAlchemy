import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
# engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=True)
engine = create_engine("sqlite:////Users/Clare/Desktop/RUTSOM201810DATA5-master/RUTSOM201810DATA5-master/02-Homework/10-Advanced-Data-Storage-and-Retrieval/Instructions/Resources/hawaii.sqlite", echo=True)
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
        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/")

# Finding the 12-month dates
# last_measurement_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
# fixed_last_measurement_date = dt.datetime.strptime(last_measurement_date[0], '%Y-%m-%d')
# first_measurement_date = (fixed_last_measurement_date) - dt.timedelta(days=365)

# Create the precipitation webpage
@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').all()
    prcp_dict = dict(prcp_results)
    return jsonify(prcp_dict) 
    
# Create the station webpage
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of station data """
    # Query all stations
    #station_results = session.query(Station.station).all()
    station_results = session.query(Measurement.station).\
        group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).all()
    # Convert list of tuples into normal list
    station_list = list(np.ravel(station_results))
    return jsonify(station_list)

# Create the tobs webpage
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of tobs data """
    # Query all tobs
    tobs_results = session.query(Station.name, Measurement.date,Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23',
        Measurement.date <= '2017-08-23').all()
    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(tobs_results))
    return jsonify(tobs_list)




if __name__ == '__main__':
    app.run(debug=True)