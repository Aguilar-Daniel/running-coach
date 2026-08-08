from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.extensions import db
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
    errors = ProfileUpdateSchema().validate(edit_request)
    if errors:
        return jsonify({'error': errors}), 400
    for key in edit_request:
        setattr(field_owner(key, user.profile, user), key, edit_request[key])
    db.session.commit() 
    attributes = serialize_profile(user)   
    return jsonify(attributes)        