from app.extensions import db

class PersonalRecord(db.Model):
    __tablename__ = "personal_records"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    distance_category = db.Column(db.Enum('1mi', '2mi', '5k', '10k', 'half_marathon', 'marathon', name='distance_category'), nullable=False)
    run_id = db.Column(db.Integer, db.ForeignKey('runs.id'), nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False)
    __table_args__ = (
        db.UniqueConstraint('user_id', 'distance_category', name='uq_user_records'), #Makes it so one user can't have 2 prs for the same distance
    )
