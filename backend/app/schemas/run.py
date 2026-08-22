from marshmallow import Schema, fields, validate

class RunCreateSchema(Schema):
    distance_meters = fields.Integer(validate=validate.Range(min=1), required=True)
    duration_seconds = fields.Integer(validate=validate.Range(min=1), required=True)
    date = fields.Date(required=True)
    perceived_effort = fields.String(validate=validate.OneOf(['easy', 'moderate', 'hard']), required=False, allow_none=True)
    notes = fields.String(required=False, allow_none=True)

class RunUpdateSchema(Schema):
    distance_meters = fields.Integer(validate=validate.Range(min=1)) #nothing required so that user doesn't have to fill out every field when updating a run
    duration_seconds = fields.Integer(validate=validate.Range(min=1))
    date = fields.Date()
    perceived_effort = fields.String(validate=validate.OneOf(['easy', 'moderate', 'hard']), allow_none=True)
    notes = fields.String(allow_none=True)