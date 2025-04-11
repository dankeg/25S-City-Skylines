from flask import Blueprint, request, jsonify, make_response, current_app, redirect, url_for
import json
from backend.db_connection import db

# This blueprint handles some basic routes that you can use for testing
urbanPlanner_routes = Blueprint('urbanPlanner_routes', __name__)

# ------------------------------------------------------------
# to get all projects
@urbanPlanner_routes.route('/projects', methods=['GET'])
def get_all_projects():
    current_app.logger.info('GET /projects route')
    cursor = db.get_db().cursor()
    
    cursor.execute('''
        SELECT project_id, name, status, budget, description, 
               sustainabilityScore, timeToCompletion, region_id, department_id 
        FROM Project
    ''')  
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# ------------------------------------------------------------
# to get all departments
@urbanPlanner_routes.route('/departments', methods=['GET'])
def get_all_departments():
    current_app.logger.info('GET /departments route')
    cursor = db.get_db().cursor()
    
    cursor.execute('''
        SELECT department_id, name, budget
        FROM Department
    ''')
    
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# ------------------------------------------------------------
# to get all regions
@urbanPlanner_routes.route('/regions', methods=['GET'])
def get_all_regions():
    current_app.logger.info('GET /regions route')
    cursor = db.get_db().cursor()
    
    cursor.execute('''
        SELECT region_id, regionName as name, population
        FROM Region
    ''')
    
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# ------------------------------------------------------------
# to add a project
@urbanPlanner_routes.route('/projects', methods=['POST'])
def add_project():
    data = request.get_json()
    cursor = db.get_db().cursor()
    
    cursor.execute('''
        INSERT INTO Project (name, status, budget, description, 
                           sustainabilityScore, timeToCompletion,
                           region_id, department_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        data['name'],
        data['status'],
        data['budget'],
        data['description'],
        data['sustainabilityScore'],
        data['timeToCompletion'],
        data['region_id'],
        data['department_id']
    ))
    
    db.get_db().commit()
    return jsonify({"message": "Project added"}), 201

# ------------------------------------------------------------
# to get project locations
@urbanPlanner_routes.route('/project-locations', methods=['GET'])
def get_project_locations():
    current_app.logger.info('GET /project-locations route')
    cursor = db.get_db().cursor()
    
    # in the below query, i have used MIN latitude and longitude because
    # each region has multiple locations, so i am just getting the first one
    # otherwise it leads to multiple rows for each project 
    cursor.execute('''
        SELECT 
            p.project_id, 
            p.name, 
            p.status, 
            p.budget, 
            p.sustainabilityScore,
            MIN(l.latitude) as latitude,
            MIN(l.longitude) as longitude,
            r.regionName as region_name
        FROM Project p
        JOIN Location l ON p.region_id = l.region_id
        JOIN Region r ON p.region_id = r.region_id
        GROUP BY p.project_id, p.name, p.status, p.budget, 
                 p.sustainabilityScore, r.regionName
    ''')
        
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response
