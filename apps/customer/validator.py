from marshmallow import Schema, fields


class CustomerValidator(Schema):
    full_name = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    otp = fields.Str(required=True)


class CustomerLoginValidator(Schema):
    phone_number = fields.Str(required=True)
    password = fields.Str(required=True)


class CustomerAddFavorisValidator(Schema):
    customer_identifier = fields.Str(required=True)
    product_id = fields.Str(required=True)


class CustomerAddDeliveryAddressValidator(Schema):
    customer_identifier = fields.Str(required=True)
    address = fields.Str(required=True)
    city = fields.Str(required=True)
    phone_number = fields.Str(required=True)


class CustomerUpdatePinValidator(Schema):
    customer_identifier = fields.Str(required=True)
    password = fields.Str(required=True)
