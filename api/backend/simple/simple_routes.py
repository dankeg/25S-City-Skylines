from flask import Blueprint, request, jsonify, make_response, current_app, redirect, url_for
import json
from backend.db_connection import db
from backend.simple.playlist import sample_playlist_data

# This blueprint handles some basic routes that you can use for testing
simple_routes = Blueprint('simple_routes', __name__)


# ------------------------------------------------------------
# / is the most basic route
# Once the api container is started, in a browser, go to 
# localhost:4000/playlist
@simple_routes.route('/')
def welcome():
    current_app.logger.info('GET / handler')
    welcome_message = '<h1>Welcome to the CS 3200 Project Template REST API'
    response = make_response(welcome_message)
    response.status_code = 200
    return response

# ------------------------------------------------------------
# /playlist returns the sample playlist data contained in playlist.py
# (imported above)
@simple_routes.route('/playlist')
def get_playlist_data():
    current_app.logger.info('GET /playlist handler')
    response = make_response(jsonify(sample_playlist_data))
    response.status_code = 200
    return response

# ------------------------------------------------------------
@simple_routes.route('/niceMesage', methods = ['GET'])
def affirmation():
    message = '''
    <H1>Think about it...</H1>
    <br />
    You only need to be 1% better today than you were yesterday!
    '''
    response = make_response(message)
    response.status_code = 200
    return response

# ------------------------------------------------------------
# Demonstrates how to redirect from one route to another. 
@simple_routes.route('/message')
def mesage():
    return redirect(url_for(affirmation))


