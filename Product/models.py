from account.models import User
from django.db import models
from django.utils.text import slugify


class MainCategory(models.Model):
    cat = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.cat

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = slugify(self.cat)
        super(MainCategory, self).save()


class Category(models.Model):
    maincat = models.ForeignKey(MainCategory, on_delete=models.CASCADE, null=True)
    category = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.category

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = slugify(self.category)
        super(Category, self).save()


class Product(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, unique=True)
    brand = models.CharField(max_length=30)
    price = models.FloatField()
    description = models.TextField(null=True,blank=True)
    warranty = models.CharField(max_length=30)
    image = models.ImageField(upload_to='Media/product')
    qty = models.PositiveSmallIntegerField()
    off = models.PositiveSmallIntegerField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    off_price = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.cat}#{self.name}#{self.price}#{self.off}#{self.qty}'

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = slugify(self.name)

        self.off_price = self.price - (self.off * self.price / 100)
        super(Product, self).save()


class Brand(models.Model):
    cat = models.ForeignKey(MainCategory, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to='media/brand')

    def __str__(self):
        return self.title


class Likes(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.product},{self.user}'


class ComericalSlider(models.Model):
    name = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='slider')
    image = models.ImageField(upload_to='media')

    def __str__(self):
        return self.name.cat
