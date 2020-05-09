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
#Need to initialize measurment
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Base.classes.keys()

passenger = Base.classes.keys()

measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    resultdt = session.query(measurement.date).all()
    resultprcp= session.query(measurement.prcp).all()
    
    session.close()
   
    # Convert list of tuples into normal list
    date = list(np.ravel(resultdt))
    prcp = list(np.ravel(resultprcp))

    all_results = []
    for i in range(len(date)):
        #resultdt["Date"] = date
        #resultprcp["Prcp"] = prcp
         
        all_results.append({date[i]:prcp[i]})

    
    return jsonify(all_results)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(station.station).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #USC00519281
    
    resultd = session.query(measurement.tobs).filter(measurement.date > '2016-08-23').filter(measurement.station=='USC00519281').all()
    session.close()

    return jsonify(resultd)
  

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
     
    resultq = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date > start).all()
    session.close()

    return jsonify(resultq)
  
@app.route("/api/v1.0/<start>/<end>")
def begin(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
     
    resultb= session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).group_by(measurement.date).all()
    session.close()

    return jsonify(resultb)

if __name__ == '__main__':
    app.run(debug=True)
