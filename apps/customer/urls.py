from django.urls import path
from django.conf.urls import include
from tastypie.api import Api

from apps.customer.api.auth import AuthResource
from apps.customer.api.me import CustomerResource, ProofTypeResource, FavorisResource

resources = []

resources.append(AuthResource())
resources.append(CustomerResource())
resources.append(ProofTypeResource())
resources.append(FavorisResource())
