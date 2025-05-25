import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'workshop-parts.db')
    app.config['SECRET_KEY'] = 'alotbsol'
    
    db.init_app(app)
    os.makedirs(app.instance_path, exist_ok=True)

    # . means current package. Because app/ contains __init__.py
    # Python cosiders app/ as a package named `app`
    with app.app_context():
        from . import parts, locations, search, delete
        db.create_all()
    
    return app