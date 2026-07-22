from app.extensions import db
from app.models.user import User 
from app.models.profile import Profile 
import pytest

def test_create_user_with_profile(app):
    with app.app_context():
        user = User(
            email="runner@example.com",
            password_hash="hashed",
            unit_preference="imperial",
        )
        db.session.add(user)
        db.session.flush()

        profile = Profile(user_id=user.id, name="Test Runner")
        db.session.add(profile)
        db.session.commit() 

        fetched = User.query.filter_by(email="runner@example.com").first()
        assert fetched is not None
        assert fetched.profile.name == "Test Runner"
                #Works once db.relationship() is established 
                #bc User id will be used to know which profile to look at
                #with .profile

def test_email_must_be_unique(app):
    with app.app_context():
        db.session.add(User(email='dup@example.com', password_hash='a', unit_preference='imperial')) 
        db.session.commit()

        db.session.add(User(email='dup@example.com', password_hash='b', unit_preference='metric'))

        with pytest.raises(Exception):
            db.session.commit()           