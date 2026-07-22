from app.extensions import db
from datetime import datetime, timezone

class User(db.Model): #Inherits the database so SQLAlchemy knows this is a table def not js a class
    __tablename__ = "users" #gives the table a name
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    unit_preference = db.Column(db.Enum('metric', 'imperial',name='unit_preference'), default='metric', nullable = False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    profile = db.relationship('Profile', uselist=False)
