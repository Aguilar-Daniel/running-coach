from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from app.extensions import db
from app.models.personal_record import PersonalRecord
from app.utils import get_current_user
records_bp = Blueprint('records',__name__, url_prefix='/api/v1/records')


def serialize_records(record):
    serialized_records = {
        'distance_category': record.distance_category,
        'duration_seconds': record.duration_seconds,
        'run_id': record.run_id
    }
    return serialized_records

def create_record():
    current_user = get_current_user()
    
@records_bp.get('')
@jwt_required()
def get_all_records():
    current_user = get_current_user()
    records = {'records': [serialize_records(record) for record in PersonalRecord.query.filter_by(user_id=current_user.id).all()]} #.all() returns a list already

    return jsonify(records)

