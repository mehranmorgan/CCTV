from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart_view'),
    path('addtocart', views.ProductAddCart.as_view(), name='addtocart'),
    path('deleteitem/<str:id>', views.DeleteItemView.as_view(), name='deleteitem'),
    path('OrderCreate', views.OrderCreateView.as_view(), name='Order_create'),
    path('OrderDetail/<int:pk>', views.OrderDetailView.as_view(), name='Order_Detail'),
]
