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
allactive = Blueprint('allactive', __name__)
 
#------------------------------------------------------------
# Get all active maintenance logs from the system
@allactive.route('/active-work-orders', methods=['GET'])
def get_active_work_orders():
    current_app.logger.info('GET /active-work-orders route hit')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT 
            i.issue_id, i.issue_type, i.status, i.priority, i.description,
            l.latitude, l.longitude,
            c.crew_id, c.crew_name
        FROM CityPlanner.Issue_Log i
        JOIN CityPlanner.Location l ON i.location_id = l.location_id
        LEFT JOIN CityPlanner.Crew c ON i.crew_id = c.crew_id
        WHERE i.status IN ('Open', 'In Progress')
        ORDER BY i.priority, i.issue_id;
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    
    return jsonify(data), 200

