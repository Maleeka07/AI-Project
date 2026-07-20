# AI-Powered Movie Recommendation Feed - Main Application
from flask import Flask
from config import Config
from routes.main_routes import main_bp
from routes.api_routes import api_bp
from routes.admin_routes import admin_bp
import os


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)

    # Create upload folder for posters
    os.makedirs(os.path.join(app.static_folder, 'images'), exist_ok=True)

    return app


if __name__ == '__main__':
    app = create_app()
    print("=" * 50)
    print("  AI-Powered Movie Recommendation Feed")
    print("  Running on http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
