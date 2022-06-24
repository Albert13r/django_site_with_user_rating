from django.urls import path
from .views import *

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('top_10/', TopUsers.as_view(), name='top_10'),
    path('home/', home, name='home'),
    path('generate_invite_code/', generate_invite_code, name='generate_invite_code'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
]
