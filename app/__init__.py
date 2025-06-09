import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    '''
    Application factory function for creating and configuring the Flask app.
    This allows modular setup and is especially useful for managing configuration,
    database initialization, and blueprint registration in one place.
    '''
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'workshop-parts.db')
    app.config['SECRET_KEY'] = 'alotbsol'
    
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize the db with the Flask app
    db.init_app(app)

    with app.app_context():
        from app import models  # Register models.py
        from app.parts import bp as parts_bp
        from app.search import bp as search_bp
        from app.locations import bp as locations_bp
        

        app.register_blueprint(parts_bp)
        app.register_blueprint(search_bp)
        app.register_blueprint(locations_bp)

        db.create_all()

    return app