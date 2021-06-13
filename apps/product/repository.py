from apps.product.models import Category, Product, ProductCommandForm, TypeForm, Banner


def get_categories(status=True):
    return Category.objects.filter(status=status).select_related('parent')


def get_products(status=True):
    return Product.objects.filter(status=status)


def get_form_fields():
    return ProductCommandForm.objects.all()


def get_type_forms():
    return TypeForm.objects.all()


def get_product_by_id(id):
    return Product.objects.get(id=id)


def get_product_by_identifier(identifier):
    return Product.objects.get(identifier=identifier)


def get_banner(status=True):
    return Banner.objects.filter(status=status)
