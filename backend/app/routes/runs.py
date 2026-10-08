from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from app.extensions import db
from app.models import Run
from app.schemas.run import RunCreateSchema, RunUpdateSchema
from app.utils import get_current_user
from app.services.pace import calculate_pace_seconds_per_km 
from app.services.ownership import get_owned_run_or_404
from app.services.pr_matching import match_distance_category
from app.services.pr_updates import make_personal_record_for_run, recompute_personal_record
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
    db.session.flush() # Creates new_run.id w/o commiting
    make_personal_record_for_run(new_run)
    db.session.commit()

    return jsonify(serialize_run(new_run)), 201


@runs_bp.get('')
@jwt_required()
def get_all_runs():
    current_user = get_current_user()
    user_runs = [serialize_run(run) for run in current_user.runs]
    response = {'runs': user_runs}
    return jsonify(response), 200

@runs_bp.get('/<int:run_id>')
@jwt_required()
def get_run_with_id(run_id):
    current_user = get_current_user()
    return jsonify(serialize_run(get_owned_run_or_404(run_id,current_user.id))), 200

@runs_bp.patch('/<int:run_id>')
@jwt_required()
def edit_run(run_id):
    current_user = get_current_user()
    patch_request = request.get_json() or {}
    edited_run = get_owned_run_or_404(run_id, current_user.id)
    try:
        patch_request = RunUpdateSchema().load(patch_request) #Gives me organized data (with proper date object instead of string)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400    
    
    for key in patch_request:
        setattr(edited_run, key, patch_request[key])
    db.session.commit()
    return jsonify(serialize_run(edited_run)), 200    

@runs_bp.delete('/<int:run_id>')
@jwt_required()
def delete_run(run_id):
    current_user = get_current_user()
    run_to_delete = get_owned_run_or_404(run_id, current_user.id)
    distance_category = match_distance_category(run_to_delete.distance_meters)
    if distance_category is not None:
        recompute_personal_record(current_user.id, distance_category=distance_category, run_to_ignore=run_to_delete)
    db.session.delete(run_to_delete)
    db.session.commit()
    return '', 204