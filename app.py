import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, jsonify



engine = create_engine("sqlite:///Hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)


station = Base.classes.station
measurements = Base.classes.measurements


session = Session(engine)


app = Flask(__name__)




@app.route("/api/v1.0/precipitation")
def precipitation():
    rain = session.query(measurements.date, measurements.prcp).filter(measurements.date > ('2016-08-23'))

    rain_dict = []
    for row in rain:
        rain_dict.append({'date': row[0], 'prcp': row[1]})

    return jsonify(rain_dict)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(station.name)
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    station_activity = session.query(measurements.station, func.count(measurements.tobs)).group_by(measurements.station).order_by(func.count(measurements.tobs).desc()).all()

    

    return jsonify(station_activity)

@app.route("/api/v1.0/<start>")
def trip(start):


    session.query(func.min(measurements.tobs), func.avg(measurements.tobs), func.max(measurements.tobs)).\
    filter(measurements.date >= start)

    return jsonify(trip)
    
@app.route("/api/v1.0/<start>/<end>")
def trip_(start,end):

    session.query(func.min(measurements.tobs), func.avg(measurements.tobs), func.max(measurements.tobs)).\
    filter(measurements.date >= start).filter(measurements.date <= end).all()

    return jsonify(trip_)


