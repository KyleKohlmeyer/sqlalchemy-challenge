# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# The session is created and closed for each API route query
# instead of opening the session here and closing it at the end

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


# #################################################
# # Flask Routes
# #################################################

# Home page with all available API routes
@app.route("/")
def welcome():
    
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation | Returns jsonified precipitation(in) data for the last year<br/>"
        f"/api/v1.0/stations | Returns jsonified list of stations<br/>"
        f"/api/v1.0/tobs | Returns jsonified temp(F) data for the last year<br/>"
        f"/api/v1.0/startdate | returns min, max, and avg temp(F) after this date. startdate must be in format yyyy/mm/dd<br/>"
        f"/api/v1.0/startdate/enddate | returns min, max, and avg temp for this range. startdate and enddate must be in format yyyy/mm/dd"
    )
    
# Page with precipitation data
@app.route("/api/v1.0/precipitation")
def prcpdata():
    
    """Return a list of all precipitation data for the last year"""
    # Query for most recent year of precipitation data
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).\
                      filter(Measurement.date >= dt.datetime(2016, 8, 23)).\
                      order_by(Measurement.date).all()

    session.close()

    # Create empty list
    prcp_data = []
    # Append each datapoint to the list
    for date, prcp, in results:
        prcp_dict = {"Date": "prcp"}
        prcp_dict["Date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)
    # Return jsonified precipitation data
    return jsonify(prcp_data)

# Page with station data    
@app.route("/api/v1.0/stations")
def stationinfo():
    
    """Return a list of all station data"""
    # Query for all stations and their ID
    session = Session(engine)
    results = session.query(Station.station, Station.id).all()
    session.close()

    # Create empty list
    station_data = []
    
    # Append each datapoint to the list
    for station, id, in results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["ID"] = id
        station_data.append(station_dict)

    # Return jsonified precipitation data
    return jsonify(station_data)
    

# Page with temperature data
@app.route("/api/v1.0/tobs")
def tobsdata():

    """Return a list of all temperature data for the last year"""
    # Query for all temperature data within the last year
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).\
                           filter(Measurement.date >= dt.datetime(2016, 8, 23)).\
                           order_by(Measurement.date).all()
    session.close()

    # Create empty list
    tobs_data = []

    # Append each datapoint to the list
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["Temperature"] = tobs
        tobs_data.append(tobs_dict)

    # Return jsonified temperature data
    return jsonify(tobs_data)

# Page for finding temperature data after the given start date    
@app.route("/api/v1.0/<start>")
def startinfo(start):

    """Return a list of the temperature statistics after the provided date"""
    
    session = Session(engine)
    # Define functions for min, max, and avg
    sel = [Measurement.station, 
           func.min(Measurement.tobs), 
           func.max(Measurement.tobs), 
           func.avg(Measurement.tobs)]
    
    # Query for all temperatures after the provided start date
    temp_start = session.query(*sel).\
                   filter(Measurement.date >= start).all()
    session.close() 

    # Create empty list     
    start_stats = []

    # Append the statistics from the query to the list
    for station, min, max, avg in temp_start:
        start_dict = {}
        start_dict["Station"] = station
        start_dict["Min_Temperature"] = min
        start_dict["Max_Temperature"] = max
        start_dict["Avg_Temperature"] = avg
        start_stats.append(start_dict)

    # Return jsonified statistics
    return jsonify(start_stats)

# Page for finding temperature data between the given dates
@app.route("/api/v1.0/<start>/<end>")
def startendinfo(start, end):

    """Return a list of the temperature statistics between the provided dates"""
    
    session = Session(engine)

    # Define functions for min, max, and avg
    sel = [Measurement.station, 
           func.min(Measurement.tobs), 
           func.max(Measurement.tobs), 
           func.avg(Measurement.tobs)]
    
    # Query for all temperatures between the provided dates
    temp_start_end = session.query(*sel).\
                   filter(Measurement.date >= start).\
                   filter(Measurement.date <= end).all()
    session.close()

     # Create empty list   
    start_end_stats = []

    # Append the statistics from the query to the list
    for station, min, max, avg in temp_start_end:
        start_end_dict = {}
        start_end_dict["Station"] = station
        start_end_dict["Min_Temperature"] = min
        start_end_dict["Max_Temperature"] = max
        start_end_dict["Avg_Temperature"] = avg
        start_end_stats.append(start_end_dict)

    # Return jsonified statistics
    return jsonify(start_end_stats)

# Debugging
if __name__ == '__main__':
    app.run(debug=True)


