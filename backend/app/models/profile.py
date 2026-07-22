from app.extensions import db

class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    sex = db.Column(db.Enum('male', 'female', name='sex'), nullable=True)
    #name in .Enum gives a name to the list of options
    experience_level = db.Column(db.Enum('beginner', 'intermediate', 'advanced', name='user_experience'), nullable=True)