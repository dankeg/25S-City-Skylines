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
updatinglog = Blueprint('updatinglog', __name__)
 
#------------------------------------------------------------


# udating completed job
@updatinglog.route('/updatinglog', methods=['POST'])
def log_completed_maintenance():
    current_app.logger.info('POST /maintenance-logs')

    data = request.json
    description = data.get('description')
    issue_id = data.get('issue_id')
    log_id = data.get('log_id')

    if not description or not issue_id:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        cursor = db.get_db().cursor()
        
        # Insert new maintenance log
        insert_query = '''
            INSERT INTO CityPlanner.Maintenance_Log (description, completed_date, issue_id, log_id)
            VALUES (%s, CURRENT_TIMESTAMP, %s, %s)
        '''
        cursor.execute(insert_query, (description, issue_id, log_id))

        # Update issue status to 'Completed'
        update_query = '''
            UPDATE CityPlanner.Issue_Log
            SET status = 'Completed'
            WHERE issue_id = %s
        '''
        cursor.execute(update_query, (issue_id,))
        
        db.get_db().commit()

        return jsonify({'message': 'Maintenance job logged and issue marked as completed'}), 201

    except Exception as e:
        db.get_db().rollback()
        return jsonify({'error': str(e)}), 500
# List all active issues in a table (from GET /active-work-orders)
# Each row has a “✔ Done” button next to it
# When clicked, a small modal or inline text area appears to input a description
# Submit the form → triggers POST
