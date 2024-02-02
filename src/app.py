from flask import render_template, make_response, jsonify
import connexion
from flask_migrate import Migrate as FlaskMigrate
from config import Config
config_obj = Config.load()
from core.database import database
import pathlib
from flask_cors import CORS



basedir = pathlib.Path(__file__).parent.resolve()
connexion_app = connexion.App(__name__, specification_dir=basedir)
connexion_app.app.config.from_object(config_obj)
connexion_app.add_api(basedir / "api/v1/swagger.yml")
connexion_app.add_api(basedir / "core/authentication/swagger.yml")
app = connexion_app.app

CORS(app, origins=["http://localhost:3000"])


db=database.initialize(
    configuration=config_obj.DATABASE, application=connexion_app
)

# Set up migrations
_ = FlaskMigrate(app, db, compare_type=True)


@app.route("/")
def home():
    return render_template("home.html")


@app.errorhandler(404)
def not_found(error):
    
    return make_response(jsonify({"error": "not found"}), 404)

@app.errorhandler(500)
def server_error(error):
    
    return make_response(jsonify({"error": "Internal Server Error"}), 500)

@app.errorhandler(400)
def bad_request(error):
    
    return make_response(jsonify({"error": "Bad Request"}), 400)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config_obj.LISTEN_PORT, debug=config_obj.DEBUG)