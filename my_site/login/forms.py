from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from .models import SiteUser
from django.core import validators
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


def validate_invite_code(value):
    try:
        SiteUser.objects.get(personal_invite_code=value)
    except ObjectDoesNotExist:
        raise ValidationError(
            _('"%(value)s" is not a valid invite code'),
            params={'value': value},
        )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               required=False)


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    invite_code = forms.CharField(label='Invite code', error_messages={'required': 'please input an invite code'},
                                  widget=forms.TextInput(attrs={'class': 'form-control'}), required=False,
                                  validators=[validate_invite_code, validators.validate_slug])

    class Meta:
        model = SiteUser
        fields = ['username', 'email', 'invite_code']
