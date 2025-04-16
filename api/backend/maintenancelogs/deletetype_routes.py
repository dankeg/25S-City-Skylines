from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db


deletecompleted = Blueprint('deletecompleted', __name__)
 
@deletecompleted.route('/infrastructure_type/<issue_id>', methods=['DELETE'])
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

@deletecompleted.route('/infrastructure_types', methods=['GET'])
def get_all_infrastructure_types():
    current_app.logger.info(f'DELETE /infrastructure_types')

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
