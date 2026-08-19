from app.extensions import db
from datetime import datetime, timezone

class Run(db.Model):
    __tablename__ = 'runs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    distance_meters = db.Column(db.Float, nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    perceived_effort = db.Column(db.Enum('easy', 'moderate', 'hard', name='perceived_effort'), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    user = db.relationship('User', backref='runs')
