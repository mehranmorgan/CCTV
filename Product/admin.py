from django.contrib import admin
from .models import Category, Product, MainCategory, Brand, Likes, ComericalSlider, WishList

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(MainCategory)
admin.site.register(Likes)
admin.site.register(ComericalSlider)
admin.site.register(WishList)
