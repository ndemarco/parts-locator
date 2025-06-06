from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint
from app import db



class Parts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    # Keep legacy free form location text for now
    location = db.Column(db.String(200), nullable=False)
    # Structured location reference (optional)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True, index=True)
    location_ref = db.relationship('Location', backref='parts')
    mcmaster_id = db.Column(db.String(15))
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Part {self.id}: {self.description}>"
    
class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False, index=True)
    layer = db.Column(db.String, nullable=False)
    row = db.Column(db.Integer, nullable=False)
    column = db.Column(db.String, nullable=False)
    sub_index = db.Column(db.Integer)
    multi_slot = db.Column(db.Boolean, default=False)
    label_text = db.Column(db.Text)

    module_obj = db.relationship('Module', backref='locations')

    location_definition_id = db.Column(db.Integer, db.ForeignKey('location_definitions.id'))
    definition_ref = db.relationship('LocationDefinition', backref='locations')

    __table_args__ = (
        UniqueConstraint('module_id', 'layer', 'row', 'column', 'sub_index', name='uix_location'),
    )

    def __repr__(self) -> str:
        loc = f"{self.layer}:{self.row}{self.column}"
        if self.sub_index is not None:
            loc += f".{self.sub_index}"
        module_name = self.module_obj.name if self.module_obj else self.module_id
        return f"<Location {module_name}-{loc}>"

class LocationDefinition(db.Model):
    __tablename__ = "location_definitions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    json_data = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))




    class Module(db.Model):
    __tablename__ = "modules"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)  # Place to hold the geographic location of a module

    def __repr__(self) -> str:
        return f"<Module {self.name}>"

