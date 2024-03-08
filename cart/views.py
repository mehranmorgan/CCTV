from django.shortcuts import render, redirect
from django.views import View

from Product.models import Product
from .cart_session import Cart
from .models import Order, OrderItem


# Create your views here.
class CartView(View):
    def get(self, request):
        cart = Cart(request)
        for x in cart:
            print(x)
        return render(request, 'cart/shopping-cart.html', {'cart': cart})


class ProductAddCart(View):
    def post(self, request):
        pk = int(request.POST.get('product_pk'))
        qty = request.POST.get('qty')
        cart = Cart(request)
        cart.add(pk=pk, qty=qty)
        return redirect('cart:cart_view')


class DeleteItemView(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('cart:cart_view')


class OrderCreateView(View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total=cart.total())
        for item in cart:
            orderitem = OrderItem.objects.create(order_id=order.id, product=item['product'], qty=item['qty'],
                                                 price=float(item['price']))

        return redirect('cart:Order_Detail', order.id)


class OrderDetailView(View):
    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        return render(request, 'cart/oreder_detail.html', {'order': order})
