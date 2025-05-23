from app.part_locator import app, db, Parts
from datetime import datetime, timezone
from flask import redirect, render_template

@app.route('/delete/<int:id>')
def delete(id):
    part = Parts.query.get_or_404(id)

    part.deleted_at = datetime.now(timezone.utc)

    try:
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem marking the part as deleted."

@app.route('/deleted')
def view_deleted():
    deleted_parts = Parts.query.filter(Parts.deleted_at != None).order_by(Parts.deleted_at.desc()).all()
    return render_template('deleted.html', parts=deleted_parts)

@app.route('/undelete/<int:id>', methods=['POST'])
def undelete(id):
    part = Parts.query.get_or_404(id)
    part.deleted_at = None

    try:
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem restoring the part."