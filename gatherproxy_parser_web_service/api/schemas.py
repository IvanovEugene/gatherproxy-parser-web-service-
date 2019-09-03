from marshmallow import Schema, fields


class CollectRequestSchema(Schema):
    url = fields.String(data_key="url-to-parse",
                        description="URL from which proxies will be collected")
    page_count = fields.Integer(data_key="page-count",
                                description="Count of pages to collect")
    validate = fields.Boolean(data_key="check-to-validity",
                              description="Flag which responsible for proxy")
