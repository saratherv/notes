

# External Imports
import connexion
import os 
import requests
import atexit
from enum import Enum 

# Project Imports 
from flask_sqlalchemy import SQLAlchemy

class DatabaseType(Enum):
    LOCAL = 0
    CLOUD = 1

db = SQLAlchemy()


def initialize(configuration: dict, application: connexion.FlaskApp):
    
    application.app.app_context().push()

    # Validates supported engine type
    configuration["engine"] = DatabaseType[configuration.get("engine")]

    if configuration.get("engine") == DatabaseType.LOCAL:
        application.app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "mysql+pymysql://{user}:{pw}@{host}:{port}/{database_name}?charset=utf8mb4".format(
            user = configuration.get("username"),
            pw = configuration.get("password"),
            host = configuration.get("host"),
            port = configuration.get("port", 3306),
            database_name = configuration.get("dbname", "notes_db")
        )
    elif configuration.get("engine") == DatabaseType.CLOUD:
        application.app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "mysql+pymysql://{user}:{pw}@{host}:{port}/{database_name}?charset=utf8mb4".format(
            user = configuration.get("username"),
            pw = configuration.get("password"),
            host = configuration.get("host"),
            port = configuration.get("port", 3306),
            database_name = configuration.get("dbname", "notes_db")
        )

    else: # Configuration not available yet eventhough valid type
        raise Exception(f"Invalid Engine type: {configuration.get('engine')}")
    
    db.init_app(application.app)

    @application.app.after_request 
    def after_request_function(response):
        db.session.close()
        return response

    return db
