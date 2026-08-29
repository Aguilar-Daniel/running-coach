from app.models import Run
from app.extensions import db
from flask import abort
def get_owned_run_or_404(run_id, user_id):
    run = db.session.get(Run, run_id)
    if run is None or run.user_id != user_id:
        abort(404)
    return run    
