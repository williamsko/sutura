from apps.transaction import repository
from apps.customer import controller as customer_controller
from apps.product import controller as product_controller
from apps.product.models import Product
from apps.utils.exceptions import ProductException, PayloadException
from apps.transaction.validator import CommandValidator
from marshmallow import ValidationError


def get_all_items():
    return repository.get_all_items()


def get_all_commands():
    return repository.get_all_commands()


def create_or_get_command(payload):
    try:
        _validate_command_payload(payload)
    except ValidationError as e:
        raise PayloadException(str(e))
    customer_identifier = payload.get('customer_identifier')
    customer = customer_controller.get_customer_by_identifier(
        customer_identifier)
    return repository.create_or_get_command(customer, payload.get('command_identifier', None))


def add_item_to_command(payload, command):
    product_identifier = payload.get('product_identifier')
    try:
        product = product_controller.get_product_by_identifier(
            product_identifier)
    except Product.DoesNotExist:
        raise ProductException('Produit introuvable')

    details = payload.get('details')

    repository.add_item_to_command(command, product, details)


def _validate_command_payload(payload):
    validator = CommandValidator()
    validator.load(payload)
