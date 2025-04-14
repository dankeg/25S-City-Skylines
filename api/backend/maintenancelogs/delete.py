########################################################
# 
########################################################
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
maintenancelogs = Blueprint('maintenancelogs', __name__)
 
#------------------------------------------------------------
# Get all maintenance logs from the system
@maintenancelogs.route('/maintenance-logs', methods=['GET'])
def get_all_maintenance_logs():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT log_id, completed_date, ml.description, ml.issue_id, il.status
                    FROM CityPlanner.Maintenance_Log ml
                    INNER JOIN CityPlanner.Issue_Log il
                    ON il.issue_id = ml.issue_id
                    WHERE il.status = 'Open' OR il.status = 'In Progress'
                    ORDER BY il.status
    ''')
    
    logs_data = cursor.fetchall()
    
    response = make_response(jsonify(logs_data))
    response.status_code = 200
    return response

#------------------------------------------------------------
# post the maintenance logs
@maintenancelogs.route('/maintenance-logs', methods=['POST'])
def post_maintenance_log():
    current_app.logger.info('POST /maintenance-logs route')
    
    # Get the JSON data from the request
    log_data = request.json
    
    # Extract the required fields from the JSON data
    log_id = int(log_data['log_id'])
    #completed_date = log_data['completed_date']
    description = log_data['description']
    issue_id = int(log_data['issue_id'])

    current_app.logger.info("I AM BEING LOGGED")
    current_app.logger.info(log_id)
    current_app.logger.info(description)
    current_app.logger.info(issue_id)

    
    # Create the SQL query for inserting a new maintenance log
    query = '''
    INSERT INTO CityPlanner.Maintenance_Log 
    (log_id, completed_date, description, issue_id, status)
    VALUES (%s, CURRENT_TIMESTAMP, %s, %s, 'Open')
    '''
    
    # Create the data tuple for the query
    data = (log_id, description, issue_id)
    
    # Execute the query
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    
    # Get the ID of the newly inserted log
    new_logid = cursor.lastrowid
    
    # Commit the transaction
    db.get_db().commit()
    
    # Return a success response with the new log ID
    return jsonify({
        'message': 'Maintenance log created successfully',
        'log_id': new_logid
    }), 201  # 201 Created status code

#------------------------------------------------------------
# Get customer detail for customer with particular userID
#   Notice the manner of constructing the query. 


@maintenancelogs.route('/maintenance-logs/<int:log_id>', methods=['DELETE'])
def delete_maintenance_log(log_id):
    try:
        cursor = db.get_db().cursor()
        
        # First check if the log exists
        cursor.execute('''SELECT log_id 
                          FROM Maintenance.MaintenanceLogs 
                          WHERE log_id = %s''', 
                       (log_id,))
        
        if not cursor.fetchone():
            response = make_response(jsonify({"error": "Maintenance log not found"}))
            response.status_code = 404
            return response
            
        # Delete the maintenance log
        cursor.execute('''DELETE FROM Maintenance.MaintenanceLogs 
                          WHERE log_id = %s''', 
                       (log_id,))
        
        db.get_db().commit()
        
        response = make_response(jsonify({"message": f"Maintenance log {log_id} successfully deleted"}))
        response.status_code = 200
        return response
        
    except Exception as e:
        db.get_db().rollback()
        response = make_response(jsonify({"error": str(e)}))
        response.status_code = 500
        return response