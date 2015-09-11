from django.db import models
from django.contrib.auth.models import User
from django.core import serializers
from elasticsearch import Elasticsearch
import datetime

class Product(models.Model):
    name       = models.TextField()
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()
#    created_by = models.ForeignKey(User, db_column='user_id')
    is_active  = models.BooleanField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.is_active = True
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return super(Product, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.unindex()
        return super(Product, self).delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        es = Elasticsearch()
        json = {
            'product_id': self.id,
            'product_name': self.name,
            'is_product_active': self.is_active,
            'indexed_at': datetime.datetime.now(),
            'variants': list(map(lambda v: {
                'variant_name': v.name,
                'variant_color': v.color,
                'is_variant_active': v.is_active,
            }, Variant.objects.filter(product=self)))
        }
        es.index(
            index    = 'ecommerce',
            doc_type = 'product',
            id       = str(self.id),
            body     = json
        )
        return self
    def search(*args, **kwargs):
        es = Elasticsearch()
        query = kwargs.get('query', {'match_all': {}})
        size = kwargs.get('size', 10)
        sort = kwargs.get('sort', ['_score'])
        results = es.search(
            index    = 'ecommerce',
            doc_type = 'product',
            body     = {
                'query': query,
                'size': size,
                'sort': sort,
            }
        )
        return map(lambda x: x['_source'], results['hits']['hits'])
    def unindex(self):
        es = Elasticsearch()
        es.delete(
            index    = 'ecommerce',
            doc_type = 'product',
            id       = str(self.id)
        )
        return self
    def es_map():
        es = Elasticsearch()
        es.indices.put_mapping(
            index = 'ecommerce',
            doc_type = 'product',
            body = {
                'product': {
                    'properties': {
                        'variants': {
                            'type': 'nested',
                            'properties': {
                                'variant_name': { 'type': 'string' },
                                'variant_color': { 'type': 'string' },
                            }

                        }
                    }
                }
            }
        )

class Variant(models.Model):
    product    = models.ForeignKey(Product)
    name       = models.TextField()
    color      = models.TextField()
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()
#    created_by = models.ForeignKey(User, db_column='user_id')
    is_active  = models.BooleanField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.datetime.now()
            self.is_active = True
        self.updated_at = datetime.datetime.now()
        return super(Variant, self).save(*args, **kwargs)