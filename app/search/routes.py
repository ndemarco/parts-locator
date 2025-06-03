from flask import request, jsonify
from . import bp
from app.models import Parts
from sqlalchemy import or_

@bp.route('/api/search')
def search_api():
    query = request.args.get('q', '')

    base_query = Parts.query
    if query:
        base_query = base_query.filter(
            or_(
            Parts.description.ilike(f'%{query}%'),
            Parts.location.ilike(f'%{query}%'),
            Parts.mcmaster_id.ilike(f'%{query}%')
            )
        )
    # Filter soft_deleted parts
    base_query = base_query.filter(Parts.deleted_at.is_(None))

    matches = base_query.order_by(Parts.date_created).all()

    return jsonify([
        {
            "id": part.id,
            "description": part.description,
            "location": part.location,
            "date_created": part.date_created.strftime("%Y-%m-%d")
        }
        for part in matches
    ])