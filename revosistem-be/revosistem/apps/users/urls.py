from django.urls import path
from apps.users.views import users_dashboard

urlpatterns = [
    path('dashboard/', users_dashboard, name='users_dashboard'),
]
