# Import necessary modules and libraries
from flask import Flask, jsonify
import datetime as dt
import sqlalchemy
from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

# Create an app instance
app = Flask(__name__)

# Create an engine to connect to the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to the classes
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create a session
session = Session(engine)

# Define routes
@app.route("/")
def home():
    return (
        f"Welcome to the Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd (Replace yyyy-mm-dd with start date)<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd (Replace yyyy-mm-dd with start and end dates)"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query for precipitation data and create a dictionary
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = (dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)).date()

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    precipitation_dict = {date: prcp for date, prcp in results}

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Query for stations and return a JSON list of stations
    stations = session.query(Station.station).all()
    station_list = [station[0] for station in stations]

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query for temperature observations and return a JSON list
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(desc(func.count(Measurement.station))).first()[0]
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    print(most_recent_date)
    one_year_ago = (dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)).date()

    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station, Measurement.date >= one_year_ago).all()

    temperature_dict = {date: tobs for date, tobs in results}

    return jsonify(temperature_dict)

# Add routes for /api/v1.0/<start> and /api/v1.0/<start>/<end>

# Run the app if the script is executed directly
if __name__ == "__main__":
    app.run(debug=True)