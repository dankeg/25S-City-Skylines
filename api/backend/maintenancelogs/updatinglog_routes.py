from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

updatinglog = Blueprint('updatinglog', __name__)
 

@updatinglog.route('/updatinglog', methods=['POST'])
def log_completed_maintenance():
    current_app.logger.info('POST /maintenance-logs')

    data = request.json
    description = data.get('description')
    issue_id = data.get('issue_id')
    
    if not description or not issue_id:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        cursor = db.get_db().cursor()
        
        insert_query = '''
            INSERT INTO CityPlanner.Maintenance_Log (description, completed_date, issue_id)
            VALUES (%s, CURRENT_TIMESTAMP, %s)
        '''
        cursor.execute(insert_query, (description, issue_id))


        return jsonify({'message': 'Maintenance job logged and issue marked as completed'}), 201

    except Exception as e:
        db.get_db().rollback()
        return jsonify({'error': str(e)}), 500