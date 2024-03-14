from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, TemplateView, CreateView

from Product.models import Product, Category, MainCategory, Brand, Likes, ComericalSlider


# Create your views here.
def home(request):
    brands = Brand.objects.all()
    Comerical = ComericalSlider.objects.all()
    return render(request, 'index.html', {'brands': brands, 'comerical': Comerical})


def shop_grid(request, category_slug):
    sort = request.GET.get('sort')
    category = Category.objects.get(slug=category_slug)
    products = Category.objects.get(slug=category_slug).product_set.order_by('price')
    print(products)
    page = request.GET.get('page')
    print(page)
    paginator = Paginator(products, 15)
    page_list = paginator.get_page(page)
    return render(request, 'shop-grid.html', {'category': category, 'products': page_list})


def product_detail(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    if Likes.objects.filter(product__slug=product_slug, user_id=request.user.id).exists():
        is_like = True
    else:
        is_like = False
    return render(request, 'product-detail.html', {'product': product, 'is_like': is_like})


def shop_grid_cat(request, maincat_slug):
    MAINCATS = MainCategory.objects.get(slug=maincat_slug).category_set.all()
    print(MAINCATS)
    page = request.GET.get('page')
    print(page)
    paginator = Paginator(MAINCATS, 4)
    page_list = paginator.get_page(page)
    return render(request, 'shop-grid.html', {'products': page_list})


def like(request, product_id):
    try:
        like = Likes.objects.get(product_id=product_id, user_id=request.user.id)
        like.delete()
        return JsonResponse({'response': 'unliked'})

    except:
        like = Likes.objects.create(product_id=product_id, user_id=request.user.id)
        return JsonResponse({'response': 'liked'})


class ProductDetail(DetailView):
    template_name = 'product-detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Likes.objects.filter(product__slug=self.slug_field, user_id=self.request.user.id).exists():
            is_like = True
        else:
            is_like = False
        context['is_like'] = is_like
        return context


class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['commercial'] = ComericalSlider.objects.all()

        return context


class ProductsAllGrid(View):

    def get(self, request, slug):
        product_list = []
        maincat = MainCategory.objects.get(slug=slug)
        MAINCATS=MainCategory.objects.all()
        for cat in maincat.category_set.all():
            for pro in cat.product_set.all():
                product_list.append(pro)
        filter_param = request.GET.get('filter')
        print(filter_param)
        if filter_param:
            if filter_param != 'none':
                product_list = []
                for cat in maincat.category_set.filter(category__icontains=filter_param):
                    for pro in cat.product_set.all():
                        product_list.append(pro)
            else:
                return render(request, 'product_all_grid.html', {'products': product_list, 'maincat': maincat})
        return render(request, 'product_all_grid.html', {'products': product_list, 'maincat': maincat,'MAINCATS':MAINCATS})
