from django.urls import path
from . import views

app_name = 'Product'

urlpatterns = [
    path('wish_list', views.UserWishList.as_view(), name='wish_list'),
    path('add_to_wish', views.AdToWish.as_view(), name='add_to_wish'),

]
