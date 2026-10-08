from app.extensions import db
from app.models.personal_record import PersonalRecord
from app.services.pr_matching import match_distance_category
from app.models import Run
def make_personal_record_for_run(run):
    distance_category = match_distance_category(run.distance_meters)
    if distance_category is None:
        return
    current_record = PersonalRecord.query.filter_by(user_id=run.user_id, distance_category=distance_category).first() #Returns row or none
    if current_record is None:
        new_record = PersonalRecord(user_id=run.user_id,
        distance_category=distance_category,
        duration_seconds=run.duration_seconds,
        run_id=run.id
        )
        db.session.add(new_record) #new record being made so add() is needed
    else:
        if run.duration_seconds < current_record.duration_seconds:
            current_record.duration_seconds = run.duration_seconds
            current_record.run_id = run.id #no add here since the query already tracked the current_record
        else:
            return

def recompute_personal_record(user_id, distance_category, run_to_ignore=None):
    user_runs = [run for run in Run.query.filter_by(user_id=user_id).all() if match_distance_category(run.distance_meters) == distance_category and run != run_to_ignore]
    existing_record = PersonalRecord.query.filter_by(user_id=user_id, distance_category=distance_category).first()
    if len(user_runs) == 0:
        if existing_record:
            db.session.delete(existing_record)
    else:
        fastest_run = min(user_runs, key=lambda run: run.duration_seconds)
        if existing_record is None:
            new_record = PersonalRecord(user_id=fastest_run.user_id,
            distance_category=distance_category,
            duration_seconds=fastest_run.duration_seconds,
            run_id=fastest_run.id
            )
            db.session.add(new_record)
        else:
            existing_record.run_id = fastest_run.id
            existing_record.duration_seconds = fastest_run.duration_seconds