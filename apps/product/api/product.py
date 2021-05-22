from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from django.conf.urls import url
from tastypie.utils import trailing_slash
from apps.product import controller as product_controller
from apps.utils.exceptions import CustomerException
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpNotFound, HttpCreated, HttpApplicationError, HttpConflict
from tastypie.authorization import Authorization
from mptt.templatetags.mptt_tags import cache_tree_children
from marshmallow import ValidationError
from tastypie.fields import ToManyField, ForeignKey

from apps.product.api.category import CategoryResource


class ProductCommandFormResource(ModelResource):

    def dehydrate_initial_values(self, bundle):
        if bundle.data['initial_values']:
            return bundle.data['initial_values'].split(';')
        return []

    class Meta:
        queryset = product_controller.get_product_form_fields()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']


class TypeFormResource(ModelResource):
    form = ToManyField(ProductCommandFormResource, 'form', full=True)

    class Meta:
        queryset = product_controller.get_type_forms()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']

    def determine_format(self, request):
        return 'application/json'


class ProductResource(ModelResource):
    type_form = ForeignKey(TypeFormResource, 'type_form', full=True)
    category = ForeignKey(CategoryResource, 'category', full=True)

    class Meta:
        queryset = product_controller.get_all_products()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'products'
        filtering = {
            'slug': ALL,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'category': ALL_WITH_RELATIONS,
            'name' : ['exact', 'startswith','contains'],
        }
        authorization = Authorization()

    def determine_format(self, request):
        return 'application/json'


class BannerResource(ModelResource):
    type_form = ForeignKey(TypeFormResource, 'type_form', full=True)
    category = ForeignKey(CategoryResource, 'category', full=True)

    class Meta:
        queryset = product_controller.get_all_products()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'products'
        filtering = {
            'slug': ALL,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'category': ALL_WITH_RELATIONS,
            'name' : ['exact', 'startswith','contains'],
        }
        authorization = Authorization()

    def determine_format(self, request):
        return 'application/json'