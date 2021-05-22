from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from apps.api import urls

admin.site.site_header = 'Sutura admin'
admin.site.site_title = 'Sutura admin'
admin.site.index_title = 'Welcome to  Sutura platform administration'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urls)),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
