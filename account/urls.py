from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = 'account'

urlpatterns = [
    path('login', views.UserLogin.as_view(), name='login'),
    path('logout', views.userlogout, name='logout'),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('ContactUS', views.ContactUsMessage.as_view(), name='contactus'),
    path('pri_register', views.PhoneRegister.as_view(), name='pri_register'),
    path('verify', views.Verify.as_view(), name='verify'),
    path('AddressCheckout', views.AddressCreation.as_view(), name='addressckeckout'),
    path('myaccount', views.MyAccountView.as_view(), name='my_account'),
    path('myinformaion', views.MyInformationView.as_view(), name='my_information'),
    path('change_password', views.ChangePasswordView.as_view(), name='Change_password'),

]
