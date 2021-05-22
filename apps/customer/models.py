from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _
from apps.utils.tools import generate_random_identifier
from django.core import serializers
from apps.product.models import Product


class Customer(models.Model):

    identifier = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        default=generate_random_identifier(10),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        app_label = 'customer'

    @property
    def proofs(self):
        proofs = self.proofs_set.all()
        _ = []
        for proof in proofs:
            _.append(proof.json)
        return _

    @property
    def json(self):

        return {
            'full_name': f'{self.user.first_name} {self.user.last_name}',
            'phone_number': f'{self.user.username}',
            'email': f'{self.user.email}',
            'identifier': f'{self.identifier}',
            'mensual_limit': self.mensual_overdraft_amount,
            'balance': self.balance,
            'proofs': self.proofs,
        }

    @property
    def mensual_overdraft_amount(self):
        authorized_overdrafts = AuthorizedOverDraft.objects.filter(
            customer=self, status=True)
        if authorized_overdrafts:
            return authorized_overdrafts.last().overdraft_amount
        return 0

    @property
    def balance(self):
        balances = Balance.objects.filter(
            customer=self)
        if balances:
            return balances.last().amount
        return 0


class AuthorizedOverDraft(models.Model):
    customer = models.ForeignKey(
        'Customer', on_delete=models.DO_NOTHING, null=False, blank=False)
    overdraft_amount = models.DecimalField(
        max_digits=9, decimal_places=2, default=0, help_text=_('Overdraft amount'))
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Authorized overdraft')
        verbose_name_plural = _('Authorized overdraft')
        app_label = 'customer'


class ProofType(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    short_name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.short_name}'

    class Meta:
        verbose_name = _('Proof type')
        verbose_name_plural = _('Poofs type')
        app_label = 'customer'


class Proofs(models.Model):
    customer = models.ForeignKey(
        'Customer', on_delete=models.DO_NOTHING, null=False, blank=False)
    type = models.ForeignKey(
        'ProofType', on_delete=models.DO_NOTHING, null=False, blank=False)
    file_object = models.CharField(null=True, blank=True, max_length=100)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def json(self):
        return {
            'type': self.type,
            'status': self.status,
        }


    class Meta:
        verbose_name = _('Proof')
        verbose_name_plural = _('Proofs')
        app_label = 'customer'


class Balance(models.Model):
    customer = models.ForeignKey(
        'Customer', on_delete=models.DO_NOTHING, null=False, blank=False)
    amount = models.DecimalField(
        max_digits=9, decimal_places=2, default=0, help_text=_('Balance'))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Balance')
        verbose_name_plural = _('Balance')
        app_label = 'customer'


class Favoris(models.Model):
    customer = models.ForeignKey(
        'Customer', on_delete=models.DO_NOTHING, null=False, blank=False)
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Favoris')
        verbose_name_plural = _('Favoris')
        app_label = 'customer'

    def __str__(self):
        return f'{self.product.name} {self.customer.user.username}'
