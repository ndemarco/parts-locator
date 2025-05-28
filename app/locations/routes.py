from flask import request, render_template, redirect, url_for
from . import bp
from app.models import db, Location

@bp.route('/locations')
def list_locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

@bp.route('/locations/add', methods=['POST'])
def add_location():
    name = request.form['name']
    new_location = Location(name=name)
    db.session.add(new_location)
    db.session.commit()
    return redirect(url_for('locations.list_locations'))



