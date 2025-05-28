from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()

class Parts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    mcmaster_id = db.Column(db.String(15))
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Part {self.id}: {self.description}>"
    
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)

    __table_args__ = (UniqueConstraint('module', 'level', 'position', name='_module_level_position_uc'),)

class LocationDefinition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    json_data = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
