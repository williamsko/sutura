from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


def product_image_directory_path(instance, filename):
    return f'product/{filename}'


class Category(MPTTModel):
    name = models.CharField(max_length=20, null=False, blank=False)
    parent = TreeForeignKey('self', on_delete=models.DO_NOTHING,
                            null=True, blank=True, related_name='children')
    description = models.TextField(
        max_length=100, null=False, blank=False)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Product category')
        verbose_name_plural = _('Product category')
        app_label = 'product'


class Product(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.DO_NOTHING)
    price = models.DecimalField(
        max_digits=9, decimal_places=2, default=0, help_text=_('Product price'))
    image = models.ImageField(
        upload_to=product_image_directory_path, blank=True, null=True)
    type_form = models.ForeignKey(
        'TypeForm', null=True, blank=True, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        app_label = 'product'


FIELD_TYPE = (
    ('choices', _('Choix')),
    ('int', _('Integer')),
    ('archived', _('Archived - not available anymore')),
)


class ProductCommandForm(models.Model):
    field_name = models.CharField(
        max_length=50, null=False, blank=False)
    initial_values = models.CharField(
        max_length=50, null=True, blank=True, help_text='Put here the choices separated by a comma')
    field_type = models.CharField(
        max_length=50, null=True, blank=True, choices=FIELD_TYPE)

    def __str__(self):
        return f'{self.field_name}'

    class Meta:
        verbose_name = _('Product form field')
        verbose_name_plural = _('Product form fields')
        app_label = 'product'


class TypeForm(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    form = models.ManyToManyField('ProductCommandForm')

    class Meta:
        verbose_name = _('Product form type')
        verbose_name_plural = _('Product form type')
        app_label = 'product'

    def __str__(self):
        return self.name