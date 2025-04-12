from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
sustainability_analyst = Blueprint('sustainability_routes', __name__)


#------------------------------------------------------------
# Get all trucks from the system
@sustainability_analyst.route('/trucks', methods=['GET'])
def get_trucks():

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT truck_id, capacity, route_id
                      FROM CityPlanner.Truck
    ''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get EV and Air Quality data from the system
@sustainability_analyst.route('/ev-air-dashboard', methods=['GET'])
def get_ev_air_data():
    cursor = db.get_db().cursor()

    cursor.execute('''
        SELECT aq.AQI, aq.pollutant_type, aq.location_id, aq.station_id,
         ev.usage_level, ev.energy_consumption, ev.timestamp
        FROM CityPlanner.Air_Quality_Metrics aq
        JOIN CityPlanner.EV_Infrastructure ev ON aq.station_id = ev.station_id
        ORDER BY aq.AQI DESC
    ''')
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response
