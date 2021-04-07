from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from apps.customer import urls as customer_api_urls
from apps.product import urls as product_api_urls

admin.site.site_header = 'Sutura admin'
admin.site.site_title = 'Sutura admin'
admin.site.index_title = 'Welcome to  Sutura platform administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customer/', include(customer_api_urls)),
    path('products/', include(product_api_urls)),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
