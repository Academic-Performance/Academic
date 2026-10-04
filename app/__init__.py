import os
from flask import Flask, jsonify
from app.routes.views import views_bp
from app.routes.api import api_bp
from src.exception import CustomError

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    
    # Register blueprints
    app.register_blueprint(views_bp)
    app.register_blueprint(api_bp)

    @app.errorhandler(CustomError)
    def handle_custom_error(error):
        response = jsonify({"success": False, "error": str(error)})
        response.status_code = 400
        return response

    from werkzeug.exceptions import HTTPException
    @app.errorhandler(Exception)
    def handle_exception(error):
        if isinstance(error, HTTPException):
            return error
        response = jsonify({"success": False, "error": "An unexpected error occurred."})
        response.status_code = 500
        return response

    return app
