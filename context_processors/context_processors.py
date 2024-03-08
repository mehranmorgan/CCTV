from Product.models import MainCategory


def Maincat(request):
    MAINCATS = MainCategory.objects.all()

    return {'MAINCATS': MAINCATS}
