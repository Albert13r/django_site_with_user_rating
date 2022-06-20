import random
import string

from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from .models import SiteUser
from django.views.generic import ListView


def user_logout(request):
    logout(request)
    return redirect('login')


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # проверить is_avtive
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
                points_left = SiteUser.objects.filter(invite_code=invite_code).count()
                inviter = SiteUser.objects.get(personal_invite_code=invite_code)
                calculate(inviter, points_left)
                return render(request, "login/register.html", {"form": form})

            form.save()
            return redirect('login')

        return render(request, "login/register.html", {"form": form})
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


class TopUsers(ListView):
    model = SiteUser
    paginate_by = 10
    ordering = ['-points']


def home(request):
    user = SiteUser.objects.get(pk=request.user.pk)
    if user.personal_invite_code:
        invited_users = SiteUser.objects.filter(invite_code=user.personal_invite_code)
    else:
        invited_users = []
    return render(request, 'login/home.html', {"invited_users": invited_users, "user": user})


def generate_invite_code(request):
    user = SiteUser.objects.get(pk=request.user.pk)
    if not user.personal_invite_code:
        personal_code = "".join(random.choices(string.ascii_letters + string.digits, k=10))
        user.personal_invite_code = personal_code
        user.save()
    return redirect('home')
