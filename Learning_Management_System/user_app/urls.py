from django.urls import path
from .views import register, login, profile, delete_profile, update_profile

urlpatterns = [
    path('', login),
    path('register/', register),
    path('profile/', profile),
    path('delete/', delete_profile),
    path('update/', update_profile)
]