from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.models.personal_record import PersonalRecord
from app.utils import get_current_user
from app.routes.records import serialize_records
from app.services.pace import calculate_pace_seconds_per_km
from app.services.pr_matching import match_distance_category
import statistics as s
dashboard_bp = Blueprint('dashboard',__name__, url_prefix='/api/v1/dashboard')


def find_average_pace_per_distance_category(user_runs):
    paces_per_run_per_category = {
        '1mi': [],
        '2mi': [],
        '5k': [],
        '10k': [],
        'half_marathon': [],
        'marathon': [],
    }
    for run in user_runs:
        category = match_distance_category(run.distance_meters)
        if category is not None:
            paces_per_run_per_category[category].append(calculate_pace_seconds_per_km(run.distance_meters, run.duration_seconds))

    average_pace_per_distance_category = {
        '1mi': None,
        '2mi': None,
        '5k': None,
        '10k': None,
        'half_marathon': None,
        'marathon': None,
    }        
    for category, paces in paces_per_run_per_category.items():
        if len(paces) != 0:
            average_pace_per_distance_category[category] = s.mean(paces)       

    return average_pace_per_distance_category    
@dashboard_bp.get('')
@jwt_required()
def show_dashboard():
    current_user = get_current_user()
    total_distance_meters = sum([run.distance_meters for run in current_user.runs])
    run_count = len(current_user.runs)
    average_pace_by_category = find_average_pace_per_distance_category(user_runs=current_user.runs)

    return jsonify({
        'total_distance_meters': total_distance_meters,
        'run_count': run_count,
        'average_pace_by_category': average_pace_by_category,
        'personal_records': [serialize_records(record) for record in PersonalRecord.query.filter_by(user_id=current_user.id).all()]
        }), 200        
