from django.urls import path
from .views import *

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('top_10/', TopUsers.as_view(), name='top_10'),
]
