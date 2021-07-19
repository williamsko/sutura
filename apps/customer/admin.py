from django.contrib import admin
from apps.customer.models import Customer, Proofs, ProofType, AuthorizedOverDraft, Balance, Favoris, \
    DeliveryAddress, BankInformation, BankInstitution
from django.utils.safestring import mark_safe


def activate_customer_account(modeladmin, request, queryset):
    queryset.update(status=True)


activate_customer_account.short_description = 'Mark selected customers as active'


class CustomerAdmin(admin.ModelAdmin):

    list_display = ('identifier', 'username', 'first_name',
                    'last_name', 'address', 'status', 'balance', 'mensual_overdraft_amount')
    search_fields = ['user__first_name']
    list_filter = ('status',)
    actions = [activate_customer_account]

    def username(self, obj):
        return obj.user.username

    username.short_description = 'Phone number'

    def first_name(self, obj):
        return obj.user.first_name

    first_name.short_description = 'First name'

    def last_name(self, obj):
        return obj.user.last_name

    last_name.short_description = 'Last name'


class ProofAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'proof_preview', 'status')

    def proof_preview(self, obj):
        return mark_safe(f'<a href="{obj.file_object}">TOTO</a>')


class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'city', 'address', 'phone_number')


class BankInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'bank', 'iban', 'status')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Proofs, ProofAdmin)
admin.site.register(ProofType)
admin.site.register(AuthorizedOverDraft)
admin.site.register(Balance)
admin.site.register(Favoris)
admin.site.register(DeliveryAddress, DeliveryAddressAdmin)
admin.site.register(BankInformation, BankInformationAdmin)
admin.site.register(BankInstitution)
