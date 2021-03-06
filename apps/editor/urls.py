from django.conf.urls import include, url
from django.contrib import admin
from .controllers import product, variant

urlpatterns = [
     url(r'^product$', product.index, name='editor_product_index'),
     url(r'^product/json$', product.indexJSON, name='editor_product_index_json'),
     url(r'^product/new$', product.new, name='editor_product_new'),
     url(r'^product/(?P<product_id>\d+)$', product.show, name='editor_product_show'),
     url(r'^product/(?P<product_id>\d+)/addvariant$', variant.new, name='editor_variant_new'),
]