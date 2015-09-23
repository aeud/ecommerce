from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
import json
import logging

from apps.catalog.models import Product, Variant

def index(request):
    products = Product.objects.all()
    results = Product.search()
    return render(request, 'editor/product/index.html', {
        'products': products,
        'results': results
    })

def indexJSON(request):
    function_score = json.loads(request.GET.get('function_score', '[]'))
    results = Product.search(query={
        'function_score': function_score
#        'function_score': {
#            'functions': [
#                {
#                    'gauss': {
#                        'product_id': {
#                            'origin': 2,
#                            'scale': 1
#                        }
#                    }
#                }, {
#                    'gauss': {
#                        'product_id': {
#                            'origin': 0,
#                            'scale': 1
#                        }
#                    },
#                    'weight': 0.01
#                }
#            ],
#            'query': {
#                'query_string': {
#                    'query': 'variants.variant_id:3 OR variants.variant_id:2'
#                }
#            },
#            'min_score': 0
#        }
    })
    return HttpResponse(json.dumps(results), content_type="application/json")

def new(request):
    if request.method == 'POST':
        post_name = request.POST.get('name', None)
        p = Product(name=post_name)
        p.save()
        p.index()
        return redirect('apps.editor.controllers.product.index')
    else:
        return render(request, 'editor/product/new.html')

def show(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        variants = Variant.objects.filter(product=product)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    logger = logging.getLogger('ecommerce.analytics')
    logger.info("View %s" % str(product.name))
    return render(request, 'editor/product/show.html', {
        'product': product,
        'variants': variants,
    })
    