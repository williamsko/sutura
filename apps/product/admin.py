from django.contrib import admin

# Register your models here.
from django.contrib import admin
from apps.product.models import Category, Product, ProductCommandForm, TypeForm
from django.utils.safestring import mark_safe


class ProductCommandFormInline(admin.TabularInline):
    model = TypeForm.form.through


class ProductAdmin(admin.ModelAdmin):

    list_display = ('image_tag', 'name',  'category', 'marque',
                    'price', 'type_form', 'status')
    search_fields = ['name']
    list_filter = ('category', 'status')

    def image_tag(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return mark_safe(f'<img src="{obj.image.url}" height=100 width=100 />')


class TypeFormAdmin(admin.ModelAdmin):
    filter_horizontal = ('form',)
    inlines = [
        ProductCommandFormInline,
    ]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(TypeForm, TypeFormAdmin)
admin.site.register(ProductCommandForm)
