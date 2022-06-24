import random
import string
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .forms import UserRegisterForm, UserLoginForm
from .models import SiteUser
from django.views.generic import ListView

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator


def user_logout(request):
    logout(request)
    return redirect('login')


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'login/login.html', {"form": form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            invite_code = form['invite_code'].value()
            if invite_code:
                points_left = SiteUser.objects.filter(invite_code=invite_code).count() + 1
                inviter = SiteUser.objects.get(personal_invite_code=invite_code)
                calculate(inviter, points_left)

            uidb64 = urlsafe_base64_encode(force_bytes(SiteUser.pk))
            domain = get_current_site(request).domain
            token = token_generator.make_token(user=SiteUser)
            link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
            activate_url = f'http://{domain}{link}'
            send_mail(
                'Activate account',
                f'Hello {form["username"].value()} Click on this link to activate your account\n{activate_url}',
                'zeynalov_albert@ukr.net',
                [form['email'].value()],
                fail_silently=False
            )

            user = form.save()
            # user.is_active = False
            user.activation_code = uidb64 + token
            user.save()

        return redirect('login')
    else:
        form = UserRegisterForm()
        users_count = SiteUser.objects.count()
        if users_count >= 5:
            form.fields['invite_code'].required = True
        return render(request, "login/register.html", {"form": form})


def calculate(user: SiteUser, points: int):
    if points:
        user.points += 1
        points -= 1
        user.save()
    if points and user.invite_code:
        target_user = SiteUser.objects.get(personal_invite_code=user.invite_code)
        calculate(target_user, points)
    elif points and not user.invite_code:
        user.points += points
        user.save()


class TopUsers(ListView):
    model = SiteUser
    paginate_by = 10
    ordering = ['-points']


def home(request):
    user = SiteUser.objects.get(pk=request.user.pk)
    if user.invite_code:
        inviter = SiteUser.objects.get(personal_invite_code=user.invite_code)
    else:
        inviter = None
    if user.personal_invite_code:
        invited_users = SiteUser.objects.filter(invite_code=user.personal_invite_code)
    else:
        invited_users = []
    return render(request, 'login/home.html', {"invited_users": invited_users, "user": user, "inviter": inviter})


def generate_invite_code(request):
    user = SiteUser.objects.get(pk=request.user.pk)
    if not user.personal_invite_code:
        personal_code = "".join(random.choices(string.ascii_letters + string.digits, k=10))
        user.personal_invite_code = personal_code
        user.save()
    return redirect('home')


class VerificationView(View):
    def get(self, request, uidb64, token, ):
        try:
            user = SiteUser.objects.get(activation_code=uidb64 + token)
            user.is_active = True
            user.activation_code = None
            user.save()

            # if user.invite_code:
            #     points_left = SiteUser.objects.filter(invite_code=user.invite_code).count() + 1
            #     inviter = SiteUser.objects.get(personal_invite_code=user.invite_code)
            #     calculate(inviter, points_left)

            login(request, user)

            return redirect('home')
        except Exception as err:
            form = UserLoginForm()
            message = "Your activation code is invalid or expired"
            return render(request, 'login/login.html', {"message": message, "form": form})
