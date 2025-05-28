from flask import request, render_template, jsonify
from . import bp
from app.models import Parts
from sqlalchemy import or_

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        results = Parts.query.filter(
            or_(
                Parts.description.ilike(f'%{query}%'),
                Parts.location.ilike(f'%{query}%'),
                Parts.mcmaster_id.ilike(f'%{query}%')
            )
        ).order_by(Parts.date_created).all()

    else:
        results = []

    return render_template('search.html', query=query, results=results)

@bp.route('/api/search')
def search_api():
    query = request.args.get('q', '')
    limit = min(int(request.args.get('limit', 25)), 100)
    offset = int(request.args.get('offset', 0))

    base_query = Parts.query.filter(
        or_(
            Parts.description.ilike(f'%{query}%'),
            Parts.location.ilike(f'%{query}%'),
            Parts.mcmaster_id.ilike(f'%{query}%')
        )
    ).order_by(Parts.date_created)

    total = base_query.count()
    matches = base_query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "offset": offset,
        "limit": limit,
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