from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.extensions import db
from marshmallow import ValidationError
from app.utils import get_current_user
from app.models import field_owner
from app.schemas.profile import ProfileUpdateSchema
profile_bp = Blueprint('profile', __name__, url_prefix='/api/v1/profile')

def serialize_profile(user):
    attributes = {'name': None, 
    'date_of_birth': None, 
    'sex': None, 
    'experience_level': None, 
    'unit_preference': None,
    }   
    for key in attributes:
        attributes[key] = getattr(field_owner(key, user.profile, user), key)
    if attributes['date_of_birth'] is not None:
            attributes['date_of_birth'] = attributes['date_of_birth'].isoformat()
    return attributes

@profile_bp.get('/')
@jwt_required()
def get_profile():
    user = get_current_user()
    attributes = serialize_profile(user)
    return jsonify(attributes)

@profile_bp.patch('/')
@jwt_required() 
def edit_profile():
    user = get_current_user()
    edit_request = request.get_json() or {}
    try:
        profile_data = ProfileUpdateSchema().load(edit_request)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400 
    for key in profile_data:
        setattr(field_owner(key, user.profile, user), key, profile_data[key])
    db.session.commit() 
    attributes = serialize_profile(user)   
    return jsonify(attributes)        