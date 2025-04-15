from flask import Flask

from backend.system_administrator.system_administrator_routes import (
    system_administrator,
)
from backend.db_connection import db
# from backend.customers.customer_routes import customers
# from backend.products.products_routes import products
from backend.sustainability.sustainability_routes import sustainability_analyst
from backend.urbanPlanner.urbanPlanner import urbanPlanner_routes
# from backend.simple.simple_routes import simple_routes
# from backend.sustainability.sustainability_routes import sustainability_analyst
from backend.maintenancelogs.allactive_routes import allactive
from backend.maintenancelogs.updatinglog_routes import updatinglog
from backend.maintenancelogs.deletetype_routes import deletecompleted
from backend.maintenancelogs.logissue_routes import getissuenames
# from backend.simple.simple_routes import simple_routes
# from backend.urbanPlanner.urbanPlanner import urbanPlanner_routes
import os
from dotenv import load_dotenv


def create_app():
    app = Flask(__name__)
    
    # Load environment variables
    # This function reads all the values from inside
    # the .env file (in the parent folder) so they
    # are available in this file.  See the MySQL setup
    # commands below to see how they're being used.
    load_dotenv()

    # secret key that will be used for securely signing the session
    # cookie and can be used for any other security related needs by
    # extensions or your application
    # app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # # these are for the DB object to be able to connect to MySQL.
    # app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config["MYSQL_DATABASE_USER"] = os.getenv("DB_USER").strip()
    app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("MYSQL_ROOT_PASSWORD").strip()
    app.config["MYSQL_DATABASE_HOST"] = os.getenv("DB_HOST").strip()
    app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("DB_PORT").strip())
    app.config["MYSQL_DATABASE_DB"] = os.getenv(
        "DB_NAME"
    ).strip()  # Change this to your DB name

    # Initialize the database object with the settings above.
    app.logger.info("current_app(): starting the database connection")
    db.init_app(app)

    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.logger.info('current_app(): registering blueprints with Flask app object.')   
    app.register_blueprint(sustainability_analyst,    url_prefix='/s')
    app.register_blueprint(urbanPlanner_routes)
    app.register_blueprint(system_administrator, url_prefix="/sys")
    # app.register_blueprint(simple_routes)
    app.register_blueprint(allactive)
    app.register_blueprint(updatinglog)
    app.register_blueprint(deletecompleted)
    app.register_blueprint(getissuenames)
    # Blueprint for getting issue names
   # app.register_blueprint(customers,   url_prefix='/c')
    # app.register_blueprint(products,    url_prefix='/p')
    # app.register_blueprint(sustainability_analyst,    url_prefix='/s')
    # app.register_blueprint(urbanPlanner_routes)

    # Don't forget to return the app objects
    return app
