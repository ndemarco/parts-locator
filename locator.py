import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'workshop-parts.db')
db = SQLAlchemy(app)

class Parts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    mcmaster_id = db.Column(db.String(15))
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

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
        parts = Parts.query.order_by(Parts.date_created).all()
        return render_template('index.html', parts=parts)
    
@app.route('/delete/<int:id>')
def delete(id):
    part_to_delete = Parts.query.get_or_404(id)

    try:
        db.session.delete(part_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting the part."
    
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
                               
if __name__ == "__main__":
    os.makedirs(app.instance_path, exist_ok=True)

    with app.app_context():
        db.create_all()
    
    app.run(debug=True)