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


class AuthResource(ModelResource):

    class Meta:
        queryset = customer_controller.get_all_customers()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'auth'
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
            url(rf'^%s/register%s$' % (self._meta.resource_name, trailing_slash()), self.wrap_view(
                'register'), name='api_register'),

            url(rf'^%s/login%s$' % (self._meta.resource_name, trailing_slash()), self.wrap_view(
                'login'), name='api_customer_login'),
        ]

    def register(self, request, **kwargs):
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
