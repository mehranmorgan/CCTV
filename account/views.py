from django.db.models import Q
from django.views.generic import CreateView

from cart.models import Order
from .models import ContactUS, UserManager, User
from django.contrib.auth import logout, get_user_model
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse, reverse_lazy
from uuid import uuid4
from .forms import LoginForm, UserEditForm, UserCreationForm, AddressCreationFrom
from django.views.generic.base import View
from .forms import PhoneRegisterForm
from random import randint
from .utils import *
from django.utils import timezone


# def userlogin(request):
#     if request.method == 'POST':
#         form = LoginForm(data=request.POST)
#         if form.is_valid():
#             user = User.objects.get(username=form.cleaned_data.get('username'))
#             login(request, user)
#             return redirect('Home:home')
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})


def userlogout(request):
    logout(request)
    return render(request, 'index.html')


# class UserRegister(CreateView):
#     model = User
#     fields = ('username', 'first_name', 'last_name', 'email', 'password',)
#     template_name = 'register.html'
#     success_url = reverse_lazy('account:login')


class ContactUsMessage(CreateView):
    model = ContactUS
    fields = ('__all__')
    template_name = 'contact_us.html'
    success_url = reverse_lazy('account:contactus')


def user_edit(request):
    user = request.user
    forms = UserEditForm(instance=user)
    if request.method == 'POST':
        forms = UserEditForm(instance=user, data=request.POST)
        if forms.is_valid():
            forms.save()
    return render(request, 'useredit.html', {'form': forms})


class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['user'], password=cd['key'])
            if user is not None:
                login(request, user)
                return redirect('Home:home')
            else:
                form.add_error('user', 'alert')
        else:
            form.add_error('user', 'alert')

        return render(request, 'login.html', {'form': form})


class RegisterUser(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        time = timezone.now()
        if form.is_valid():
            User = get_user_model()
            UserManager = User.objects
            cd = form.cleaned_data
            new_user = UserManager.create_user(email=cd['email'], phone=cd['phone'],
                                               password=cd['password1'], )
            if new_user:
                # login(request, new_user)
                return redirect('Home:home')
            else:
                form.add_error(None, 'information not correct')
        else:
            form.add_error(None, 'information not correct')
        return render(request, 'register.html', {'form': form, 'time': time})


class PhoneRegister(View):
    def get(self, request):
        form = PhoneRegisterForm()
        return render(request, 'pri_register.html', {'form': form})

    def post(self, request):
        form = PhoneRegisterForm(request.POST)
        if form.is_valid():
            code = randint(1000, 9999)
            print(code)
            cd = form.cleaned_data
            phone = cd.get('phone')
            token = str(uuid4())
            # sms.verification({'receptor': cd.get('phone'), 'type': '1', 'template': '', 'param1': code})
            OTP.objects.create(phone=cd.get('phone'), varification_code=code, token=token)
            return redirect(reverse('account:verify') + f'?token={token}')


class Verify(View):

    def get(self, request):
        token = request.GET.get('token')
        otp = OTP.objects.get(token=token)
        phone = otp.phone
        return render(request, 'verify.html', context={'phone': phone})

    def post(self, request):
        token = request.GET.get('token')
        print(token)
        code = request.POST.get('code')
        print(code)
        try:
            register = OTP.objects.get(token=token, varification_code=code)
            register.delete()
            return redirect('account:register')

        except:
            return redirect('account:pri_register')


class AddressCreation(View):
    def get(self, request):
        form = AddressCreationFrom()
        return render(request, 'cart/check_out.html', {'form': form})

    def post(self, request):
        form = AddressCreationFrom(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('cart:Order_create')


class MyAccountView(View):
    def get(self, request):
        user = request.user
        orders = Order.objects.filter(Q(user=request.user))
        return render(request, 'dashboard/dashboard.html', {'orders': orders, 'user': user})


class MyInformationView(View):
    def get(self, request):
        user = request.user
        return render(request, 'dashboard/my-account-information.html', {'user': user})

    def post(self, request):
        user = request.user
        username = request.POST.get('username')
        if username:
            user.username = username
            user.save()
        email = request.POST['email']
        if email:
            user.email = email
            user.save()
        phone = request.POST.get('phone')
        if phone:
            user.phone = phone
            user.save()
        return redirect('account:my_information')


class ChangePasswordView(View):
    def post(self, request):
        user = request.user
        cpass = request.POST.get('cpass')
        npass = request.POST.get('npass')
        cnpass = request.POST.get('cnpass')
        print(cpass, npass, cnpass)
        if user.check_password(cpass):
            if npass == cnpass:
                user.set_password(npass)
                user.save()
        return redirect('account:my_information')