from app.extensions import jwt
from flask import jsonify

@jwt.unauthorized_loader
def no_token_present(reason):
    return jsonify({'error': 'authentication required'}), 401

@jwt.invalid_token_loader
def invalid_token(reason):
    return jsonify({'error': 'invalid authentication token'}), 401

@jwt.expired_token_loader
def expired_token(header, payload):
    return jsonify({'error': 'authentication token expired'}), 401