from flask_jwt_extended import get_jwt_identity
from app.models.user import User
from app.extensions import db
def get_current_user():
    return db.session.get(User, int(get_jwt_identity())) #Returns the entire row of the user and its columns
