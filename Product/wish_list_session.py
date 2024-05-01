from django.shortcuts import get_object_or_404

from Product.models import Product

WISH_LIST_ID = 'wish'


class WishListSession:
    def __init__(self, request):
        self.session = request.session
        wish = self.session.get(WISH_LIST_ID)
        if not wish:
            wish = self.session[WISH_LIST_ID] = {}
        self.wish = wish

    def __iter__(self):
        wish = self.wish.copy()
        for item in wish.values():
            item['product'] = Product.objects.get(id=int(item['id']))
            yield item

    def add(self, pk, qty):
        product = Product.objects.get(id=pk)
        if product.id not in self.wish:
            self.wish[product.id] = {'id': product.id, 'price': str(product.off_price), 'qty': 0}
        self.wish[product.id]['qty'] += int(qty)
        self.save()

    def save(self):
        self.session.modified = True

    def delete(self, pk):
        print(self.wish[f'{pk}'])
        if f'{pk}' in self.wish:
            del self.wish[f'{pk}']
            self.save()

