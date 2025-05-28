import os
from flask import Flask
from app.models import db

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'workshop-parts.db')
    app.config['SECRET_KEY'] = 'alotbsol'
    
    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app)

    with app.app_context():
        from app.parts import bp as parts_bp
        from app.search import bp as search_bp
        from app.locations import bp as locations_bp
        

        app.register_blueprint(parts_bp)
        app.register_blueprint(search_bp)
        app.register_blueprint(locations_bp)

        db.create_all()

    return app