from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404

from apps.catalog.models import Product, Variant 

def new(request, product_id):
    if request.method == 'POST':
        try:
            p = Product.objects.get(pk=product_id)
        except Variant.DoesNotExist:
            raise Http404('Variant does not exist')
        post_name = request.POST.get('name', None)
        post_color = request.POST.get('color', None)
        v = Variant(name=post_name, color=post_color, product=p)
        v.save()
        p.index()
        return redirect('apps.editor.controllers.product.show', product_id=p.id)