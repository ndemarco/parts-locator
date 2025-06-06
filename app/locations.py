from flask import request, flash, redirect, render_template, json
from app import db
@app.route('/locations', methods=['GET', 'POST'])
def locations():
    if request.method == 'POST':
        file = request.files.get('file')
        json_text = request.form.get('json')

        if file and file.filename.lower().endswith('.json'):
            json_text = file.read().decode('utf-8')

        try:
            data = json.loads(json_text)
            store_location_definition(json_text, data)
            flash('Location definitions updated.', 'success')
        except Exception as e:
            flash(f'Failed to parse JSON: {str(e)}', 'danger')

        return redirect('/locations')

    definition = LocationDefinition.query.order_by(LocationDefinition.date_created.desc()).first()
    return render_template('locations.html', json_data=definition.json_data if definition else '')

def store_location_definition(json_text, data):
    db.session.query(Location).delete()
    db.session.query(LocationDefinition).delete()
    db.session.commit()

    new_def = LocationDefinition(name="imported", json_data=json_text)
    db.session.add(new_def)
    db.session.commit()

    expanded = expand_locations(data)
    for module, levels in expanded.items():
        for level, positions in levels.items():
            for position in positions:
                db.session.add(Location(module=module, level=level, position=position))
    db.session.commit()

def expand_locations(data):
    result = {}
    for module, mod_data in data.items():
        result[module] = {}
        for level, positions in mod_data['levels'].items():
            if isinstance(positions, list):
                result[module][level] = positions
            elif isinstance(positions, str):
                result[module][level] = expand_series(positions)
            elif isinstance(positions, dict):
                result[module][level] = expand_series_dict(positions)
            else:
                raise ValueError(f"Invalid format for {module} -> {level}")
    return result

def expand_series(series_str):
    match = re.fullmatch(r'([A-Z])([0-9]+)-([A-Z])([0-9]+)', series_str, re.IGNORECASE)
    if match:
        start_letter, start_num, end_letter, end_num = match.groups()
        rows = [chr(c) for c in range(ord(start_letter.upper()), ord(end_letter.upper()) + 1)]
        cols = range(int(start_num), int(end_num) + 1)
        return [f"{r}{c}" for r in rows for c in cols]

    prefix = ''.join(filter(str.isalpha, series_str))
    bounds = list(map(int, filter(str.isdigit, series_str.replace(prefix, '').split('-'))))
    return [f"{prefix}{i}" for i in range(bounds[0], bounds[1]+1)]

def expand_series_dict(series_dict):
    prefix = series_dict.get("prefix")
    start, end = series_dict.get("range", [0, -1])
    return [f"{prefix}{i}" for i in range(start, end+1)]