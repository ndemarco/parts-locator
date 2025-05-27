from flask import current_app as app, request, render_template
from app.parts import Parts

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