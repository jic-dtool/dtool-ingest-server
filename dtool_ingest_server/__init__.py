from flask import Flask
from flask_cors import CORS

def create_app():

    app = Flask(__name__)
    CORS(app)

    from dtool_ingest_server import (
        uri_routes
    )

    app.register_blueprint(uri_routes.bp)

    return app
