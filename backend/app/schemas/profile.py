from marshmallow import Schema, fields, validate

class ProfileUpdateSchema(Schema):
    name = fields.String()
    date_of_birth = fields.Date()
    sex = fields.String(validate=validate.OneOf(['male', 'female']))
    experience_level = fields.String(validate=validate.OneOf(['beginner', 'intermediate', 'advanced']))
    unit_preference = fields.String(validate=validate.OneOf(['imperial', 'metric']))