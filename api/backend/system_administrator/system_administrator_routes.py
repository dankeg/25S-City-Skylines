from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    current_app,
    redirect,
    url_for,
)
import json
from backend.db_connection import db
from backend.simple.playlist import sample_playlist_data

# This blueprint handles some basic routes that you can use for testing
system_administrator = Blueprint("system_administrator", __name__)


# # ------------------------------------------------------------
# # / is the most basic route
# # Once the api container is started, in a browser, go to
# # localhost:4000/playlist
# @system_administrator.route("/")
# def welcome():
#     current_app.logger.info("GET / handler")
#     welcome_message = "<h1>Welcome to the CS 3200 Project Template REST API"
#     response = make_response(welcome_message)
#     response.status_code = 200
#     return response


# # ------------------------------------------------------------
# # /playlist returns the sample playlist data contained in playlist.py
# # (imported above)
# @system_administrator.route("/playlist")
# def get_playlist_data():
#     current_app.logger.info("GET /playlist handler")
#     response = make_response(jsonify(sample_playlist_data))
#     response.status_code = 200
#     return response


# # ------------------------------------------------------------
# @system_administrator.route("/niceMesage", methods=["GET"])
# def affirmation():
#     message = """
#     <H1>Think about it...</H1>
#     <br />
#     You only need to be 1% better today than you were yesterday!
#     """
#     response = make_response(message)
#     response.status_code = 200
#     return response


# # ------------------------------------------------------------
# # Demonstrates how to redirect from one route to another.
# @system_administrator.route("/message")
# def mesage():
#     return redirect(url_for(affirmation))


@system_administrator.route("/users/<start_date>/<end_date>", methods=["GET"])
def get_users(start_date, end_date):
    cursor = db.get_db().cursor()

    cursor.execute(
        """
        SELECT * FROM Users
        WHERE last_login BETWEEN %s AND %s
        """,
        (start_date, end_date),
    )

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


@system_administrator.route("/user-tickets", methods=["GET"])
def get_user_tickets():

    cursor = db.get_db().cursor()
    cursor.execute(
        """SELECT * FROM User_Tickets
    """
    )

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


@system_administrator.route("/user-tickets/<id>", methods=["PUT", "DELETE"])
def modify_user_tickets(id):
    cursor = db.get_db().cursor()
    if request.method == "PUT":
        cursor.execute(
            """
            UPDATE User_Tickets
            SET 
                assignee_id = %s,
                description = %s,
                filer_id = %s,
                status = %s,
                title = %s
            WHERE ticket_id = %s;
        """,
            (
                request.json["assignee_id"],
                request.json["description"],
                request.json["filer_id"],
                request.json["status"],
                request.json["title"],
                id,
            ),
        )

        db.get_db().commit()
        return make_response(jsonify({"ticket_id": id}), 200)

    elif request.method == "DELETE":
        cursor.execute(
            """
            DELETE FROM User_Tickets
            WHERE ticket_id = %s;
        """,
            (id,),
        )

        db.get_db().commit()
        return make_response(jsonify({"ticket_id": id}), 200)


@system_administrator.route("/incidents", methods=["GET"])
def get_incidents():

    cursor = db.get_db().cursor()
    cursor.execute(
        """SELECT * FROM Incidents
    """
    )

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


@system_administrator.route("/monitoring-config", methods=["GET", "POST"])
def handle_monitoring_config():
    cursor = db.get_db().cursor()

    if request.method == "GET":
        cursor.execute("SELECT * FROM Monitoring_Config;")
        records = cursor.fetchall()
        the_response = make_response(jsonify(records))
        the_response.status_code = 200
        return the_response

    elif request.method == "POST":
        data = request.get_json()

        cursor.execute(
            """
            INSERT INTO Monitoring_Config (job, importance, monitor_condition, monitor_interval)
            VALUES (%s, %s, %s, %s);
            """,
            (
                data.get("job"),
                data.get("importance"),
                data.get("monitor_condition"),
                data.get("monitor_interval"),
            ),
        )
        db.get_db().commit()

        the_response = make_response(jsonify({"message": "Monitoring config added"}))
        the_response.status_code = 201
        return the_response


@system_administrator.route("/monitoring-config/<id>", methods=["PUT", "DELETE"])
def modify_monitoring_config(id):
    cursor = db.get_db().cursor()

    if request.method == "PUT":
        data = request.get_json()

        cursor.execute(
            """
            UPDATE Monitoring_Config
            SET job = %s,
                importance = %s,
                monitor_condition = %s,
                monitor_interval = %s
            WHERE config_id = %s;
            """,
            (
                data.get("job"),
                data.get("importance"),
                data.get("monitor_condition"),
                data.get("monitor_interval"),
                id,
            ),
        )
        db.get_db().commit()

        the_response = make_response(jsonify({"message": "Monitoring config updated"}))
        the_response.status_code = 200
        return the_response

    elif request.method == "DELETE":
        cursor.execute("DELETE FROM Monitoring_Config WHERE config_id = %s;", (id,))
        db.get_db().commit()

        the_response = make_response(jsonify({"message": "Monitoring config deleted"}))
        the_response.status_code = 200
        return the_response


@system_administrator.route("/monitored-incidents", methods=["GET"])
def handle_monitored_incidents():

    cursor = db.get_db().cursor()
    cursor.execute(
        """SELECT *
    FROM Monitoring_Config AS mc
    LEFT JOIN Config_Incident AS ci
        ON mc.config_id = ci.config_id
    LEFT JOIN Incidents AS i
        ON ci.incident_id = i.incident_id;
    """
    )

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response
