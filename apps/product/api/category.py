from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from django.conf.urls import url
from tastypie.utils import trailing_slash
from apps.product import controller as product_controller
from apps.utils.exceptions import CustomerException
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpNotFound, HttpCreated, HttpApplicationError, HttpConflict
from tastypie.authorization import Authorization
from mptt.templatetags.mptt_tags import cache_tree_children
from marshmallow import ValidationError


class CategoryResource(ModelResource):

    class Meta:
        queryset = product_controller.get_all_categories()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'categories'
        filtering = {
            'slug': ALL,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        excludes = ('level', 'lft', 'rght', 'tree_id', 'created', 'updated')
        authorization = Authorization()

    def determine_format(self, request):
        return 'application/json'

    def get_child_data(self, obj):
        data = {
            'id': obj.id,
            'name': obj.name,
        }
        if not obj.is_leaf_node():
            data['children'] = [self.get_child_data(child)
                                for child in obj.get_children()]
        return data

    def get_list(self, request, **kwargs):

        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle,
                                    **self.remove_api_resource_names(kwargs))
        sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(
            request.GET, sorted_objects,
            resource_uri=self.get_resource_uri(), limit=self._meta.limit,
            max_limit=self._meta.max_limit,
            collection_name=self._meta.collection_name
        )
        to_be_serialized = paginator.page()

        objects = cache_tree_children(objects)

        bundles = []

        for obj in objects:
            data = self.get_child_data(obj)
            bundle = self.build_bundle(data=data, obj=obj, request=request)
            bundles.append(self.full_dehydrate(bundle))

        to_be_serialized[self._meta.collection_name] = bundles
        to_be_serialized = self.alter_list_data_to_serialize(request,
                                                             to_be_serialized)
        return self.create_response(request, to_be_serialized)
