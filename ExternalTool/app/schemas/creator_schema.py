
from marshmallow import Schema, fields, validate

class CreatorBatchRequestSchema(Schema):
    size = fields.String(
        required=True,
        validate=validate.OneOf(['small', 'medium', 'large']),
        metadata={
            'description': 'Size of batch to generate (small=500, medium=5000, large=10000)',
            'example': 'small'
        }
    )
