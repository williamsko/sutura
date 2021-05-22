from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from django.conf.urls import url
from tastypie.utils import trailing_slash
from apps.transaction import controller as transaction_controller
from apps.utils.exceptions import ProductException, CommandException
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpNotFound, HttpCreated, HttpApplicationError, HttpConflict
from tastypie.fields import ForeignKey
from apps.product.api import ProductResource
from marshmallow import ValidationError

API_FORMAT = 'application/json'


class CommandResource(ModelResource):

    class Meta:
        queryset = transaction_controller.get_all_commands()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = ''
        filtering = {
            'identifier': ALL,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }

    def determine_format(self, request):
        return API_FORMAT

    def prepend_urls(self):
        return [
            url(r'^command/create%s$' % trailing_slash(), self.wrap_view(
                'create_new_command'), name='api_create_new_command'),
        ]

    def create_new_command(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        payload = self.deserialize(request, request.body)
        try:
            command = transaction_controller.create_or_get_command(
                payload)
            transaction_controller.add_item_to_command(payload, command)
        except CommandException as e:
            return self.create_response(request, {'error': str(e)}, HttpConflict)
        except Exception as e:
            return self.create_response(request, {'error': str(e)}, HttpApplicationError)

        except ValidationError as e:
            return self.create_response(request, {'error': str(e)}, HttpApplicationError)
        return self.create_response(request, command.identifier, HttpCreated)

    def add_item_to_command(self, request,**kwargs):
        self.method_check(request, allowed=['post'])
