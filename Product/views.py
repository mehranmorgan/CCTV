from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .models import Product
from .wish_list_session import WishListSession


# Create your views here.
class UserWishList(View):
    def get(self, request):
        wish = WishListSession(request)
        user = request.user
        return render(request, 'product/wishlist.html', {'objs': wish})


class AdToWish(View):

    def post(self, request):
        wish = WishListSession(request)
        pk = request.POST.get('pk')
        qty = request.POST.get('qty')
        product = Product.objects.get(id=int(pk))
        wish.add(pk, qty)
        return redirect('Home:product_detail', product.slug)
