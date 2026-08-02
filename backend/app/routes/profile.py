from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.utils import get_current_user
from app.models import field_owner
profile_bp = Blueprint('profile', __name__, url_prefix='/api/v1/profile')

@profile_bp.get('/')
@jwt_required()
def get_profile():
    user = get_current_user()
    attributes = {'name': None, 
    'date_of_birth': None, 
    'sex': None, 
    'experience_level': None, 
    'unit_preference': None,
    }
    for key in attributes:
        attributes[key] = getattr(field_owner(key, user.profile, user), key)
    return jsonify(attributes)
    