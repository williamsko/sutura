from marshmallow import Schema, fields


class DetailValidator(Schema):
    field_name = fields.Str(required=True)
    field_value = fields.Str(required=True)


class CommandValidator(Schema):
    customer_identifier = fields.Str(required=True)
    command_identifier = fields.Str(required=False)
    product_identifier = fields.Str(required=True)
    details = fields.List(fields.Nested(DetailValidator, required=True))
