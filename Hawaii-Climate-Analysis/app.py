import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template, abort

#creating engine to connect with hawaii sqlite database
    
engine = create_engine("sqlite:///hawaiidb.sqlite")

#using automap to load orm automatically

Base = automap_base()

# reflecting the tables from orm classes

Base.prepare(engine, reflect = True)

Measurement = Base.classes.Measurement
Station = Base.classes.Station
# print(Base.classes.keys())

#initiating session
session = Session(engine)

# initiating flask api

app = Flask(__name__)

@app.route('/')
def welcome():
    return jsonify({"Title": "Welcome to hawaii weather info app",
        "endpoints":["/api/v1.0/precipitation",
        "/api/v1.0/stations",
        "/api/v1.0/tobs",
        "/api/v1.0/<start>",
        "/api/v1.0/<start>/<end>"]})


# /api/v1.0/precipitation
# Query for the dates and precipitation observations from the last year.
# Convert the query results to a Dictionary using date as the key and tobs as the value.
# Return the json representation of your dictionary.

@app.route("/api/v1.0/precipitation")

def prcp():
    prev_year = dt.date.today() - dt.timedelta(days=365)
    # date_string = prev_year.strftime("%Y-%m-%d")

    prcp_each_day = session.query(Measurement.date,Measurement.prcp).\
                    filter(Measurement.date >= prev_year).\
                    group_by(Measurement.date).\
                    order_by(Measurement.date).all()
    
    prcp_dict = dict(prcp_each_day)
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():

    #define query
    stations = session.query(Station.station, Station.name).all()
    Measurements = session.query(Measurement.station).distinct(Measurement.station).all()

    #Create measurement list to check Stations query against
    Measurelist = []

    for row in Measurements:
        Measurelist.append(row.station)

    #Create station list composed of items from station
    Stationlist = []

    for row in stations:
        #check if the station is in the Distinct List. My way out of the lack of foreign keys.
        if row.station in Measurelist:
            station_dict = {}
            station_dict['station'] = row.station
            station_dict['name'] = row.name
            Stationlist.append(station_dict)

    #jsonify results
    return jsonify(Stationlist)

# /api/v1.0/tobs
# Return a json list of Temperature Observations (tobs) for the previous year

@app.route('/api/v1.0/tobs')

def tobs():
    """Return a json list of Temperature Observations (tobs) for the previous year"""
    prev_year = dt.date.today() - dt.timedelta(days=365)
    # date_string = prev_year.strftime("%Y-%m-%d")

    tobsquery = session.query(Measurement.tobs).filter(Measurement.date >= prev_year).all()

    tobslist = list(np.ravel(tobsquery))

    return jsonify(tobslist)

#executing the error handler page using 404 abort
@app.errorhandler(404)
def page_not_found(e):
    
    return ("<h2> 404: Page Not Found </h2>"
            "Please enter a date in database range: <b>2010-01-01</b> to <b>2017-08-23</b>"),404



@app.route('/api/v1.0/<start>', methods=["GET"])

# Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.


def tobsinfo_start(start):
    
    # daterange = [date for dates in session.query(Measurement.date).all()]
    try:
        if start:# in daterange:
            # start = func.strftime('%Y-%m-%d', 'start')

            sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

            calcs = session.query(*sel).filter(func.strftime('%Y-%m-%d',Measurement.date) >= start).one()


            return (
                f"<h2> Temperature(F) informtion from {start} </h2>"
                f"Minimum temp: {calcs[0]}<br>"
                f"Average temp: {round(calcs[1],2)}<br>"
                f"Maximum temp: {round(calcs[2],2)}<br>"
                )
    except:
        abort(404)
        

@app.route('/api/v1.0/<start>/<end>')

def tobsinfo_start_end(start,end):
    # daterange = session.query(Measurement.date).all()
    try:
        if start and end: #in daterange:
            # start = func.strftime('%Y-%m-%d', 'start')

            sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

            calcs = session.query(*sel).filter(func.strftime('%Y-%m-%d',Measurement.date).between( start,end)).one()


            return (
                f"<h2> Temperature informtion from {start} to {end}</h2>"
                f"Minimum temperature: {calcs[0]}<br>"
                f"Average temperature: {round(calcs[1],2)}<br>"
                f"Maximum temperature: {round(calcs[2],2)}<br>"
                )

    except:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
