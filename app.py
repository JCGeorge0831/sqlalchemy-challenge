# Relevant imports
from flask import Flask, jsonify

import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from datetime import datetime

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#-----------------------------
# Setting up Flask app
app = Flask(__name__)

# Flask Routes
@app.route("/")
def home():
    """Listing all available routes"""
    return (
        f"Home Page <br/> "
        f"Available API Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/cal_start_temp<br/>"
        f"/api/v1.0/cal_start_end_temp"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Querying the precipitation results
    calculating_one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > calculating_one_year).\
        order_by(Measurement.date).all()
    session.close()

    # Creating a dictionary for precipitation data
    all_prcp_inches = []
    for date,prcp in precipitation_data: 
        prcp_inch_dict = {}
        prcp_inch_dict['date'] = date
        prcp_inch_dict['prcp'] = prcp
        all_prcp_inches.append(prcp_inch_dict)
    return jsonify(all_prcp_inches)

@app.route("/api/v1.0/stations")
def stations():

    # Query the list of stations from the station csv file
    total_stations = session.query(Station.station).all()
    
    session.close()

    # Coverting into normal list
    all_stations = list(np.ravel(total_stations))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    most_active_station_id = 'USC00519281'
    
    calculating_one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    previous_year_TOBS = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.station == most_active_station_id).\
            filter(Measurement.date > calculating_one_year).\
            order_by(Measurement.date).all()
    session.close()

    all_temp_observations = []
    for date,tobs in previous_year_TOBS:
        temp_obs_dict = {}
        temp_obs_dict['date'] = date
        temp_obs_dict['tobs'] = tobs
        all_temp_observations.append(temp_obs_dict)
    return jsonify(all_temp_observations)

@app.route("/api/v1.0/cal_start_temp")
def cal_start_temp():
    start = datetime.strptime('2016-08-24', '%Y-%m-%d').date()
    start_temp_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    start_temp_obs = []
    for min, max, avg in start_temp_results:
       start_temp_dict = {}
       start_temp_dict['TMIN'] = min
       start_temp_dict['TMAX'] = max
       start_temp_dict['TAVG'] = avg
       start_temp_obs.append(start_temp_dict)
    
    return jsonify(start_temp_obs)

@app.route("/api/v1.0/cal_start_end_temp")
def cal_start_end_temp():
    start = datetime.strptime('2016-08-24', '%Y-%m-%d').date() 
    end = datetime.strptime('2017-08-23', '%Y-%m-%d').date()
    start_end_temp_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    start_end_temp_obs = []
    for min, max, avg in start_end_temp_results:
        start_end_temp_dict = {}
        start_end_temp_dict['TMIN'] = min
        start_end_temp_dict['TMAX'] = max
        start_end_temp_dict['TAVG'] = avg
        start_end_temp_obs.append(start_end_temp_dict)
    
    return jsonify(start_end_temp_obs)

if __name__ == '__main__':
    app.run(debug=True)

                    




