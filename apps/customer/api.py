from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from django.conf.urls import url
from tastypie.utils import trailing_slash
from apps.customer import controller as customer_controller
from apps.utils.exceptions import CustomerException, ProductException
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpNotFound, HttpCreated, HttpApplicationError, HttpConflict
from tastypie.authorization import Authorization
from tastypie.fields import ForeignKey
from apps.product.api import ProductResource
from marshmallow import ValidationError
from apps.utils.api import MultiPartResource

API_FORMAT = 'application/json'


class ProofTypeResource(ModelResource):

    class Meta:
        queryset = customer_controller.get_all_proof_types()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'proof_types'
        filtering = {
            'slug': ALL,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        authorization = Authorization()

    def determine_format(self, request):
        return API_FORMAT


class CustomerResource(MultiPartResource, ModelResource):

    class Meta:
        queryset = customer_controller.get_all_customers()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = ''
        filtering = {
            'slug': ALL,
            'identifier': ALL,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        authorization = Authorization()

    def determine_format(self, request):
        return API_FORMAT

    def prepend_urls(self):
        return [
            url(r'^create%s$' % trailing_slash(), self.wrap_view(
                'create_new_customer'), name='api_create_new_customer'),
            url(r'^login%s$' % trailing_slash(), self.wrap_view(
                'login'), name='api_customer_login'),
            url(r'^upload%s$' % trailing_slash(), self.wrap_view(
                'upload_file'), name='api_upload_file'),
            url(r'^favoris/add%s$' % trailing_slash(), self.wrap_view(
                'add_product_to_favoris'), name='api_add_product_to_favoris'),
        ]

    def create_new_customer(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        payload = self.deserialize(request, request.body)
        try:
            response = customer_controller.new_customer(payload)
        except CustomerException as e:
            return self.create_response(request, {'error': str(e)}, HttpConflict)
        except Exception as e:
            return self.create_response(request, {'error': str(e)}, HttpApplicationError)

        except ValidationError as e:
            return self.create_response(request, {'error': str(e)}, HttpApplicationError)
        return self.create_response(request, response, HttpCreated)

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        payload = self.deserialize(request, request.body)
        try:
            response = customer_controller.customer_login(payload)
        except CustomerException as e:
            return self.create_response(request, {'error': str(e)}, HttpUnauthorized)
        except Exception as e:
            return self.create_response(request, {'error': str(e)}, HttpApplicationError)
        return self.create_response(request, response)

    def upload_file(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        _payload = self.deserialize(
            request, request.body, 'multipart/form-data')
        payload = _payload.dict()

        proof = request.FILES['proof']
        proof_type = payload.get('type')
        identifier = payload.get('identifier')
        try:
            response = customer_controller.add_proof_to_customer_account(
                identifier, proof_type, proof)
        except CustomerException as e:
            return self.create_response(request, {'error': str(e)}, HttpForbidden)
        except Exception as e:
            return self.create_response(request, {'error': str(e)}, HttpApplicationError)

        return self.create_response(request, response, HttpCreated)

    def add_product_to_favoris(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        payload = self.deserialize(request, request.body)
        try:
            response = customer_controller.add_product_to_customer_favoris(payload)
        except ProductException as e:
            return self.create_response(request, {'error': str(e)}, HttpApplicationError)
        except CustomerException as e:
            return self.create_response(request, {'error': str(e)}, HttpUnauthorized)
        except Exception as e:
            return self.create_response(request, {'error': str(e)}, HttpApplicationError)
        return self.create_response(request, response, HttpCreated)


class FavorisResource(ModelResource):
    customer = ForeignKey(CustomerResource, 'customer', null=True, full=True)
    product = ForeignKey(ProductResource, 'product', null=True, full=True)

    class Meta:
        queryset = customer_controller.get_all_favoris()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'favoris'
        filtering = {
            'slug': ALL,
            'customer': ALL_WITH_RELATIONS,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        authorization = Authorization()

    def determine_format(self, request):
        return API_FORMAT
