from django.contrib import admin
from apps.customer.models import Customer, Proofs, ProofType, AuthorizedOverDraft, Balance, Favoris
from django.utils.safestring import mark_safe


class CustomerAdmin(admin.ModelAdmin):

    list_display = ('identifier', 'username', 'first_name',
                    'last_name', 'address', 'status')
    search_fields = ['user__first_name']
    list_filter = ('status',)

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
        return mark_safe(f'<a href="{obj.content.url}">TOTO</a>')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Proofs, ProofAdmin)
admin.site.register(ProofType)
admin.site.register(AuthorizedOverDraft)
admin.site.register(Balance)
admin.site.register(Favoris)
