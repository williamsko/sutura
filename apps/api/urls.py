from apps.transaction import urls as transaction_api_urls
from django.urls import path
from django.conf.urls import include
from tastypie.api import Api

from apps.customer.urls import AuthResource, CustomerResource
from apps.product.api import CategoryResource, ProductResource

v1_api = Api(api_name='v1')
v1_api.register(AuthResource())
v1_api.register(CustomerResource())

v1_api.register(CategoryResource())
v1_api.register(ProductResource())


urlpatterns = [
    path('', include(v1_api.urls)),
]
