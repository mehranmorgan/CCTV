from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from django.forms import ValidationError
from . import models
from django import forms
from django.contrib.auth import authenticate
from django.core import validators


# class LoginForm(forms.Form):
#     username = forms.CharField(min_length=4, max_length=30,
#                                widget=forms.TextInput(
#                                    attrs={'class': 'input-text required-entry', 'placeholder': 'UserName'}))
#     password = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={'class': 'input-text required-entry validate-password', 'placeholder': 'Password'}))
#
#     def clean_password(self):
#         user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
#         user=User.objects.get(username=self.cleaned_data.get('username'))
#         print(user.password)
#         if user.password == self.cleaned_data.get('password'):
#             return self.cleaned_data.get('password')
#         else:
#             raise ValidationError('username or password is incorect', code='invalid username or password')


class LoginForm(forms.Form):
    user = forms.CharField(max_length=50, label='Phone or Email')
    key = forms.CharField(max_length=30, label='Password', validators=[validators.MaxLengthValidator(11)])

    def clean_key(self):
        user = self.cleaned_data.get('user')
        key = self.cleaned_data.get('key')
        account = authenticate(username=user, password=key)
        if account is not None:
            return key
        else:
            raise ValidationError('username or password is incorrect', code='user or pass')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('__all__')


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput,
    )

    class Meta:
        model = models.User
        fields = ["email", "phone"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.User
        fields = ["email", "password", "phone", "is_active", "is_admin"]


class PhoneRegisterForm(forms.Form):
    phone = forms.CharField(validators=[validators.MaxLengthValidator(11)])


class AddressCreationFrom(forms.ModelForm):
    class Meta:
        model = models.Address
        exclude = ['user']
