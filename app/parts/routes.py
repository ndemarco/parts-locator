from flask import render_template, request, redirect, url_for, jsonify
from . import bp
from app.models import db, Parts
from datetime import datetime, timezone


@bp.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        part_description = request.form['description']
        part_location = request.form['location']
        new_part = Parts(description=part_description, location=part_location)

        try:
            db.session.add(new_part)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your new part."

    else:
        parts = Parts.query.filter(Parts.deleted_at == None).order_by(Parts.date_created).all()
        return render_template('index.html', parts=parts)
    
@bp.route('/parts/new', methods=['GET', 'POST'])
def new_part():
    return_to = request.form.get('returnTo') or url_for('parts.index')
    if request.method == 'POST':
        description = request.form['description']
        location = request.form['location']
        part = Parts(description=description, location=location)
        db.session.add(part)
        db.session.commit()
        return redirect(return_to)

    return render_template('part_form.html')

@bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update_part(id):
    return_to = request.form.get('returnTo') or url_for('parts.index')
    part = Parts.query.get_or_404(id)
    if request.method == 'POST':
        part.description = request.form['description']
        part.location = request.form['location']

        try:
            db.session.commit()
            return redirect(return_to)
        except Exception as e:
            return 'There was an issue updating the part.'
    else:
        return render_template('part_form.html', part=part, action='update')
    
  
    
@bp.route('/delete/<int:id>')
def delete_part(id):
    part_to_delete = Parts.query.get_or_404(id)
    part_to_delete.deleted_at = datetime.now(timezone.utc)
    db.session.commit()
    return redirect(url_for('parts.index'))

@bp.route('/view_deleted_parts')
def view_deleted():
    deleted_parts = Parts.query.filter(Parts.deleted_at != None).order_by(Parts.deleted_at.desc()).all()
    return render_template('deleted.html', parts=deleted_parts)

@bp.route('/undelete/<int:id>', methods=['POST'])
def undelete(id):
    part = Parts.query.get_or_404(id)
    part.deleted_at = None

    try:
        db.session.commit()
        return redirect(url_for('parts.view_deleted_parts'))
    except:
        return "There was a problem restoring the part."
