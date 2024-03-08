from django.contrib import admin
from .models import Category, Product, MainCategory, Brand,Likes

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(MainCategory)
admin.site.register(Likes)
