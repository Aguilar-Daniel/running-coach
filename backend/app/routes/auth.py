from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, unset_jwt_cookies
from app.extensions import db, bcrypt
from app.models.user import User
from app.models.profile import Profile
from app.schemas.auth import RegisterSchema, LoginSchema
from app.utils import get_current_user

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth_bp.post('/register')
def register():
    register_request = request.get_json() or {}
    errors = RegisterSchema().validate(register_request)
    if errors:
        return jsonify({'error': errors}), 400

    existing_user = User.query.filter_by(email=register_request['email']).first()
    if existing_user:
        return jsonify({'error': 'email already registered'}), 400
    password = register_request['password']
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')    
    user = User(email=register_request['email'],password_hash=password_hash)
    db.session.add(user)
    db.session.flush()
    profile = Profile(name=register_request['name'], user_id=user.id)
    db.session.add(profile)
    db.session.commit()

    return jsonify({'id': user.id, 'email': user.email}), 201

@auth_bp.post('/login')
def login():
    login_request = request.get_json() or {}
    errors = LoginSchema().validate(login_request)
    if errors:
        return jsonify({'error': errors}), 400
    
    user = User.query.filter_by(email=login_request['email']).first()
    if user is None or not bcrypt.check_password_hash(user.password_hash, login_request['password']):
        return jsonify({'error': 'invalid email or password'}), 401
    
    jwt_token = create_access_token(identity=str(user.id))

    response = make_response(jsonify({'id': user.id, 'email': user.email}), 200)
    set_access_cookies(response, jwt_token)

    return response

@auth_bp.get('/me')
@jwt_required()
def me():
    user = get_current_user()
    return jsonify({'id': user.id, 'email': user.email}) #No need for code 200 since its the default code returned

@auth_bp.post('/logout')
# no jwt_required since expired cookies would never reach this point otherwise
def logout():
    response = make_response(jsonify({'message': 'logging out'}))
    unset_jwt_cookies(response)

    return response