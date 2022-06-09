from django.urls import path
from .views import *

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('user_profile/', TopUsers.as_view(), name='user_profile'),
]
