from apps.product import repository


def get_all_categories():
    return repository.get_categories()


def get_all_products():
    return repository.get_products()


def get_product_form_fields():
    return repository.get_form_fields()


def get_type_forms():
    return repository.get_type_forms()


def get_product_by_identifier(identifier):
    return repository.get_product_by_identifier(identifier)


def get_banner():
    return repository.get_banner()
