from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from django.conf.urls import url
from tastypie.utils import trailing_slash
from apps.customer import controller as customer_controller
from apps.utils.exceptions import CustomerException, ProductException
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpNotFound, \
    HttpCreated, HttpApplicationError, HttpConflict, HttpNoContent
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
            url(rf'^%s/register$' %
                self._meta.resource_name, self.wrap_view('register')),

            url(rf'^%s/login$' %
                self._meta.resource_name, self.wrap_view('login')),

            url(rf'^%s/request_otp$' %
                self._meta.resource_name, self.wrap_view('request_otp')),

            url(rf'^%s/update_pin$' %
                self._meta.resource_name, self.wrap_view('update_pin')),

            url(rf'^%s/reset_pin$' %
                self._meta.resource_name, self.wrap_view('update_pin')),
        ]

    def register(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        payload = self.deserialize(request, request.body)
        try:
            is_otp_valid = customer_controller.check_otp(payload)
            if not is_otp_valid:
                return self.create_response(request, {'error': 'OTP invalide'}, HttpUnauthorized)
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

    def request_otp(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        payload = self.deserialize(request, request.body)
        try:
            customer_controller.send_otp(payload)
        except Exception as e:
            return self.create_response(request, {'error': str(e)}, HttpApplicationError)
        return self.create_response(request, {}, HttpNoContent)

    def update_pin(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        payload = self.deserialize(request, request.body)
        try:
            customer_controller.update_pin(payload)
        except Exception as e:
            return self.create_response(request, {'error': str(e)}, HttpApplicationError)
        return self.create_response(request, {}, HttpNoContent)

    def reset_pin(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        payload = self.deserialize(request, request.body)
        try:
            is_otp_valid = customer_controller.check_otp(payload)
            if not is_otp_valid:
                return self.create_response(request, {'error': 'OTP invalide'}, HttpUnauthorized)

            customer_controller.update_pin(payload)
        except Exception as e:
            return self.create_response(request, {'error': str(e)}, HttpApplicationError)
        return self.create_response(request, {}, HttpNoContent)
