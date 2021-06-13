from marshmallow import Schema, fields


class DetailValidator(Schema):
    field_name = fields.Str(required=True)
    field_value = fields.Str(required=True)


class ItemsValidator(Schema):
    product = fields.Str(required=True)
    details = fields.List(fields.Nested(DetailValidator, required=True))


class CommandValidator(Schema):
    customer = fields.Str(required=True)
    command = fields.Str(required=False)
    items = fields.List(fields.Nested(ItemsValidator, required=True))
