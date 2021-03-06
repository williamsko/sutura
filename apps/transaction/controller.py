from apps.transaction import repository
from apps.customer import controller as customer_controller
from apps.product import controller as product_controller
from apps.product.models import Product
from apps.utils.exceptions import ProductException, PayloadException, CommandNotFoundException
from apps.transaction.validator import CommandValidator
from marshmallow import ValidationError
from apps.transaction.models import Command


def get_all_items():
    return repository.get_all_items()


def get_all_commands():
    return repository.get_all_commands()


def create_or_get_command(payload):
    try:
        _validate_command_payload(payload)
    except ValidationError as e:
        raise PayloadException(str(e))
    customer_identifier = payload.get('customer')
    customer = customer_controller.get_customer_by_identifier(
        customer_identifier)
    return repository.create_or_get_command(customer, payload.get('command', None))


def add_items_to_command(payload, command):
    items = payload.get('items')
    for item in items:
        try:
            product = product_controller.get_product_by_identifier(
                item.get('product'))
            details = item.get('details')
            repository.add_item_to_command(command, product, details)
        except Product.DoesNotExist:
            raise ProductException('Produit introuvable')

    payload.update({'command': command.identifier,
                    'total_amount': command.total_amount})
    return payload


def _validate_command_payload(payload):
    validator = CommandValidator()
    validator.load(payload)


def save_command_with_detail(command, payload):
    repository.update_command_details(command, payload)


def get_command_by_identifier(payload):
    command_identifier = payload.get('command_identifier')
    try:
        return repository.get_command(command_identifier)
    except Command.DoesNotExist:
        raise CommandNotFoundException()


def update_command_status(command, dest_status):
    command.status = dest_status
    command.save()


def update_command_payload(command, payload):
    payload.update({'status': command.status,
                    'delivery_date': command.created})
    return payload
