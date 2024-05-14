from django.urls import path
from .views import update_profile, register

urlpatterns = [
    path('', update_profile, name='update_profile'),
    path('register/', register, name='register'),
]

app_name = 'user_management'
