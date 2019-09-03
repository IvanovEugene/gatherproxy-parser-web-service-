from marshmallow import Schema, fields


# Config Schemas
class AppSettingsSchema(Schema):
    log_file_path = fields.String(data_key="log_file_path")
    log_level = fields.Integer(data_key="log_level")
    parser_max_workers = fields.Integer(data_key="parser_max_workers")
    host = fields.String(data_key="host")
    port = fields.Integer(data_key="port")


class DriverParamsSchema(Schema):
    driver_path = fields.String(data_key="driver_path")
    timeout = fields.Integer(data_key="timeout")


class ValidatorParamsSchema(Schema):
    verification_link = fields.String(data_key="verification_link")
    timeout = fields.Integer(data_key="timeout")


class ConfigSchema(Schema):
    app_settings = fields.Nested(nested=AppSettingsSchema,
                                 data_key="app_settings")
    driver_params = fields.Nested(nested=DriverParamsSchema,
                                  data_key="driver_params")
    validator_params = fields.Nested(nested=ValidatorParamsSchema,
                                     data_key="validator_params")
