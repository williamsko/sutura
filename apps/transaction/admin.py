from django.contrib import admin
from apps.transaction.models import Command, Item
from django.utils.safestring import mark_safe


class CommandAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'customer', 'details', 'status')
    search_fields = ['customer__username']
    list_filter = ('status', )

    def item_details(self, obj):
        html = ''
        for product in obj.details.get('products'):
            html += '<ul>'
            for detail in product.get('details'):
                html += f"<li> {product['field_name']} : {product['field_value']} </li>"
        html += '</ul>'
        return mark_safe(html)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'item_details', 'total_amount')
    search_fields = ['command__identifier']

    def item_details(self, obj):
        html = '<ul>'
        for detail in obj.details:
            html += f"<li> {detail['field_name']} : {detail['field_value']} </li>"
        html += '</ul>'
        return mark_safe(html)


admin.site.register(Command, CommandAdmin)
admin.site.register(Item, ItemAdmin)
