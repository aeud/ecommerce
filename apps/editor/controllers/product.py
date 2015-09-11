from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404

from apps.catalog.models import Product, Variant

def index(request):
    products = Product.objects.all()
    results = Product.search(query={'match_all': {}}, size=5, sort=[{'indexed_at': 'desc'}])
    return render(request, 'editor/product/index.html', {
        'products': products,
        'results': results
    })

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
    return render(request, 'editor/product/show.html', {
        'product': product,
        'variants': variants,
    })
    