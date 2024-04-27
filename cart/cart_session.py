
from django.shortcuts import get_object_or_404

from Product.models import Product

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()
        for item in cart.values():
            item['product'] = Product.objects.get(id=int(item['id']))
            item['total'] = float(item['price']) * int(item['qty'])
            yield item

    def add(self, pk, qty):
        product = get_object_or_404(Product, id=pk)
        if product.id not in self.cart:
            self.cart[product.id] = {'id': product.id, 'price': str(product.price), 'qty': 0}
        self.cart[product.id]['qty'] += int(qty)
        self.save()

    def delete(self, id):
        if id in self.cart:
            del self.cart[id]
            self.save()

    def total(self):
        cart = self.cart.values()
        total = 0
        for item in cart:
            total += float(item['price']) * int(item['qty'])
        return total

    def save(self):
        self.session.modified = True
