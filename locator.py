import os
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'workshop-parts.db')
db = SQLAlchemy(app)

from sqlalchemy import DateTime

class Parts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    mcmaster_id = db.Column(db.String(15))
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Part {self.id}: {self.description}>"
    
@app.route('/', methods=['POST', 'GET'])
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

    
@app.route('/delete/<int:id>')
def delete(id):
    part = Parts.query.get_or_404(id)

    part.deleted_at = datetime.now(timezone.utc)

    try:
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem marking the part as deleted."

    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    part = Parts.query.get_or_404(id)
    if request.method == 'POST':
        part.description = request.form['description']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating the part.'
    else:
        return render_template('update.html', part=part)
    
@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        results = Parts.query.filter(Parts.description.ilike(f'%{query}%')).order_by(Parts.date_created).all()
    else:
        results = []

    return render_template('search.html', query=query, results=results)

@app.route('/api/search')
def api_search():
    query = request.args.get('q', '')
    if not query:
        return {"results": []}

    matches = Parts.query.filter(
        Parts.description.ilike(f"%{query}%")
    ).order_by(Parts.date_created).limit(10).all()

    return {
        "results": [
            {
                "id": p.id,
                "description": p.description,
                "location": p.location,
                "created": p.date_created.strftime("%Y-%m-%d")
            }
            for p in matches
        ]
    }

@app.route('/update-inline/<int:id>', methods=['POST'])
def update_inline(id):
    data = request.get_json()
    part = Parts.query.get_or_404(id)

    part.description = data.get('description', part.description)
    part.location = data.get('location', part.location)

    try:
        db.session.commit()
        return jsonify({'success': True})
    except:
        return jsonify({'success': False}), 500

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


                               
if __name__ == "__main__":
    os.makedirs(app.instance_path, exist_ok=True)

    with app.app_context():
        db.create_all()
    
    app.run(debug=True)