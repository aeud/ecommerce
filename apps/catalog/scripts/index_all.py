from apps.catalog.models import Product

def run():
    products = Product.objects.all()
    for product in products:
        product.index()