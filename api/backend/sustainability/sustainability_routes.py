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
# User Story 2: Get EV and Air Quality data from the system
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

#------------------------------------------------------------
# User Story 1: Get all CO2 Emissions data along with Building emissions data 
# AND Add new building energy level data 
@sustainability_analyst.route('/co2-building-emissions', methods=['GET', 'POST'])
def handle_co2_building_emissions():
    cursor = db.get_db().cursor()

    if request.method == 'GET':
        cursor.execute('''
            SELECT e.emission_id, e.source, e.building_id,
                   e.emission_level, e.location_id, e.timestamp, 
                   b.energy_consumption AS building_energy_level
            FROM CityPlanner.CO2_Emissions e
            JOIN CityPlanner.Building b ON e.building_id = b.building_id
            ORDER BY e.timestamp DESC
        ''')
        data = cursor.fetchall()
        response = make_response(jsonify(data))
        response.status_code = 200
        return response

    elif request.method == 'POST':
        data = request.get_json()
        cursor.execute('''
            INSERT INTO CityPlanner.CO2_Emissions 
            (source, emission_level, timestamp, location_id, building_id)
            VALUES (%s, %s, %s, %s, %s)
        ''', (
            data.get('source', 'building_meter'),
            data.get('emission_level'),
            data.get('timestamp'),             
            data.get('location_id'),
            data.get('building_id')            
        ))

        db.get_db().commit()
        response = make_response(jsonify({"message": "CO₂ building emission added successfully"}))
        response.status_code = 201
        return response

#-----------------------------------------------------------
