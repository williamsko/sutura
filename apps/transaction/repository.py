from apps.transaction.models import Item, Command


def get_all_items():
    return Item.objects.all()


def get_all_commands():
    return Command.objects.all()


def create_or_get_command(customer, command_identifier=None):
    if command_identifier:
        return Command.objects.get(identifier=command_identifier)
    command = Command()
    command.status = 'EN_COURS'
    command.customer = customer
    command.save()
    return command


def add_item_to_command(command, product, details):
    item = Item()
    item.command = command
    item.product = product
    item.details = details
    item.save()
