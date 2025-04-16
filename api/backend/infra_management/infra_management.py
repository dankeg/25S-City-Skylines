from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

infra = Blueprint('infra_management', __name__)
 
@infra.route('/active-work-orders', methods=['GET'])
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

@infra.route('/infrastructure_type/<issue_id>', methods=['DELETE'])
def delete_infrastructure_type(issue_id):
    current_app.logger.info(f'DELETE /deletecompleted/{int(issue_id)}')

    try:
        cursor = db.get_db().cursor()

        
        delete_type = '''
            DELETE FROM CityPlanner.Infrastructure_Type
            WHERE issue_id = %s and location_id is NOT NULL
        '''
        cursor.execute(delete_type, (issue_id))
        db.get_db().commit()
        
        
        return jsonify({
            'message': f'Infrastructure type {issue_id} deleted successfully'
        }), 200

    except Exception as e:
        db.get_db().rollback()
        return jsonify({'error': str(e)}), 500

@infra.route('/infrastructure_types', methods=['GET'])
def get_all_infrastructure_types():
    current_app.logger.info(f'GET /infrastructure_types')

    try:
        cursor = db.get_db().cursor()
        get_all_query = '''
            SELECT type_id, issue_id, type, location_id, priority 
            FROM CityPlanner.Infrastructure_Type
        '''
        cursor.execute(get_all_query)

        data = cursor.fetchall()
        
        return jsonify(data), 200
    except Exception as e:
        db.get_db().rollback()
        return jsonify({'error': str(e)}), 500
    
@infra.route('/issue-names', methods=['GET'])
def fetch_issue_names():
    current_app.logger.info('GET /issue-names')
    try:
        cursor = db.get_db().cursor()

        query = '''
            SELECT il.issue_id, il.issue_type
            FROM CityPlanner.Issue_Log il
            
        '''

        cursor.execute(query)
        rows = cursor.fetchall()

        return jsonify(rows), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching issue names: {e}")
        return jsonify({'error': str(e)}), 500
    

@infra.route('/updatinglog', methods=['POST'])
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
        db.get_db().commit()

        return jsonify({'message': 'Maintenance job logged and issue marked as completed'}), 201

    except Exception as e:
        db.get_db().rollback()
        return jsonify({'error': str(e)}), 500