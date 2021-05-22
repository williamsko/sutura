from django.urls import path
from django.conf.urls import include
from tastypie.api import Api

from apps.transaction.api import CommandResource
v1_api = Api(api_name='api')

v1_api.register(CommandResource())


urlpatterns = [
    path('', include(v1_api.urls)),
]
