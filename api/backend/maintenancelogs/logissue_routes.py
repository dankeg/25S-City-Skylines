from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db


# Blueprint for getting issue names
getissuenames = Blueprint('getissuenames', __name__)


@getissuenames.route('/issue-names', methods=['GET'])
def fetch_issue_names():
    current_app.logger.info('GET /issue-names')
    try:
        cursor = db.get_db().cursor()

        # Use GROUP BY to get unique issue types, and MIN(issue_id) as a representative ID
        query = '''
            SELECT il.issue_id, il.issue_type
            FROM CityPlanner.Issue_Log il
            
        '''

        cursor.execute(query)
        rows = cursor.fetchall()

        # column_names = [desc[0] for desc in cursor.description]
        # result = [dict(zip(column_names, row)) for row in rows]

        return jsonify(rows), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching issue names: {e}")
        return jsonify({'error': str(e)}), 500
