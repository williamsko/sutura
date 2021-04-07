from django.urls import path
from django.conf.urls import include
from tastypie.api import Api

from apps.customer.api import CustomerResource, ProofTypeResource, FavorisResource
v1_api = Api(api_name='api')

v1_api.register(CustomerResource())
v1_api.register(ProofTypeResource())
v1_api.register(FavorisResource())


urlpatterns = [
    path('', include(v1_api.urls)),
]
