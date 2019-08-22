from marshmallow import Schema, fields


class CollectRequestSchema(Schema):
    url = fields.String(data_key="url-to-parse")
    page_count = fields.Integer(data_key="page-count")
    validate = fields.Boolean(data_key="check-to-validity")
