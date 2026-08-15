from marshmallow import Schema, fields, validate

class ProfileUpdateSchema(Schema):
    name = fields.String()
    date_of_birth = fields.Date(allow_none=True)
    sex = fields.String(validate=validate.OneOf(['male', 'female']), allow_none=True)
    experience_level = fields.String(validate=validate.OneOf(['beginner', 'intermediate', 'advanced']), allow_none=True)
    unit_preference = fields.String(validate=validate.OneOf(['imperial', 'metric']))