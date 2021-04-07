from django.urls import path
from django.conf.urls import include
from tastypie.api import Api

from apps.product.api import CategoryResource, ProductResource
v1_api = Api(api_name='api')

v1_api.register(CategoryResource())
v1_api.register(ProductResource())


urlpatterns = [
    path('', include(v1_api.urls)),
]
