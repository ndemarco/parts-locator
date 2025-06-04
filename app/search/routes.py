from flask import request, jsonify
from . import bp
from app.models import Parts
from sqlalchemy import or_

# Search parts. Return results in a JSON structure
@bp.route('/api/search')
def search_api():
    query = request.args.get('q', '')
    try:
        limit = min(int(request.args.get('limit', 50)), 200)
    except ValueError:
        limit = 50 # Fall back to the the default if not an integer.

    base_query = Parts.query
    if query:
        base_query = base_query.filter(
            or_(
            Parts.description.ilike(f'%{query}%'),
            Parts.location.ilike(f'%{query}%'),
            Parts.mcmaster_id.ilike(f'%{query}%')
            )
        )
    # Filter out soft_deleted parts
    base_query = base_query.filter(Parts.deleted_at.is_(None))

    matches = base_query.order_by(Parts.date_created).limit(limit).all()

    return jsonify([
        {
            "id": part.id,
            "description": part.description,
            "location": part.location,
            "date_created": part.date_created.strftime("%Y-%m-%d")
        }
        for part in matches
    ])