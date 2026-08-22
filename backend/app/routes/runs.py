from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from app.extensions import db
from app.models import Run
from app.schemas.run import RunCreateSchema, RunUpdateSchema
from app.utils import get_current_user
from app.services.pace import calculate_pace_seconds_per_km 
runs_bp = Blueprint('runs', __name__, url_prefix='/api/v1/runs')

def serialize_run(run):
    pace = calculate_pace_seconds_per_km(distance_meters=run.distance_meters, duration_seconds=run.duration_seconds)
    serialized_run = {
        'id': run.id,
        'distance_meters': run.distance_meters,
        'duration_seconds': run.duration_seconds,
        'date': run.date.isoformat(),
        'perceived_effort': run.perceived_effort,
        'notes': run.notes,
        'pace_seconds_per_km': pace
    }

    return serialized_run

@runs_bp.post('')
@jwt_required()
def create_run():
    current_user = get_current_user()
    create_request = request.get_json() or {}
    try:
        run_data = RunCreateSchema().load(create_request) #Gives me organized data (with proper date object instead of string)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400    
    
    new_run = Run(user_id=current_user.id,
                distance_meters=run_data['distance_meters'], 
                duration_seconds=run_data['duration_seconds'],
                date=run_data['date'],
                perceived_effort=run_data.get('perceived_effort', None),
                notes=run_data.get('notes', None))
    db.session.add(new_run)  
    db.session.commit()

    return jsonify(serialize_run(new_run)), 201

