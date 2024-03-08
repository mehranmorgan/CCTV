from django.urls import path
from . import views

app_name = 'Home'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('shop_grid_category/<slug:maincat_slug>', views.shop_grid_cat, name='shop_grid_cat'),
    path('shop_grid_slider/<slug:category_slug>', views.shop_grid, name='shop_grid_slider'),
    path('product_detail/<slug:slug>', views.ProductDetail.as_view(), name='product_detail'),
    path('like/<int:product_id>', views.like, name='like'),


]
