from django.contrib import admin
from apps.transaction.models import Command, Item
from django.utils.safestring import mark_safe


class CommandAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'customer', 'status')
    search_fields = ['customer__username']
    list_filter = ('status', )


class ItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'item_details', 'total_amount')
    search_fields = ['command__identifier']

    def item_details(self, obj):
        html = '<ul>'
        for detail in obj.details:
            html += f"<li> {detail['field_name']} : {detail['field_value']} </li>"
        html += '</ul>'
        return mark_safe(html)


admin.site.register(Command, CommandAdmin)
admin.site.register(Item, ItemAdmin)
