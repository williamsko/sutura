from django.db import models
from apps.utils.tools import generate_random_identifier
from django.utils.translation import ugettext_lazy as _
from apps.customer.models import Customer
from apps.product.models import Product
import jsonfield
STATUS = (
    ('EN_COURS', _('En cours de validation')),
    ('EN_COURS_DE_TRAITEMENT', _('En cours de traitement')),
    ('EN_COURS_DE_LIVRAISON', _('En cours de livraison')),
    ('LIVREE', _('Commande livrée')),
    ('RETOUR_MAGASIN', _('Retour en magasin')),
    ('ANNULEE', _('Commande annulée')))


class Command(models.Model):
    identifier = models.CharField(
        max_length=50, null=True, blank=True, default=(generate_random_identifier(10)))
    status = models.CharField(max_length=50, null=True,
                              blank=True, choices=STATUS)
    customer = models.ForeignKey(Customer,
                                 blank=False, null=False, on_delete=(models.DO_NOTHING))
    details = jsonfield.JSONField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def total_amount(self):
        items = Item.objects.filter(command=self)
        amount = 0
        for item in items:
            amount += item.total_amount
        return amount

    class Meta:
        verbose_name = _('Command')
        verbose_name_plural = _('Commands')
        app_label = 'transaction'

    def __str__(self):
        return self.identifier


class Item(models.Model):
    command = models.ForeignKey(Command,
                                blank=True, null=True, on_delete=(models.DO_NOTHING))
    product = models.ForeignKey(Product,
                                blank=False, null=False, on_delete=(models.DO_NOTHING))
    price = models.IntegerField(default=0, help_text=_('Product price'))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    details = jsonfield.JSONField()

    @property
    def total_amount(self):
        if self.product.type_form.name == 'DEFAULT':
            return int(self.details[0]['field_value']) * self.price
        if self.product.type_form.name == 'AIRTIME':
            output_dict = [
                x for x in self.details if x['field_name'] == 'montant']
            return int(output_dict[0]['field_value'])
        return 0

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')
        app_label = 'transaction'

    def __str__(self):
        return self.product.name
