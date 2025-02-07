from django.urls import path
from .views import (
    UserLoginView, UserRegisterView,
    DoctorLoginView, DoctorRegisterView
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('doctor/login/', DoctorLoginView.as_view(), name='doctor_login'),
    path('doctor/register/', DoctorRegisterView.as_view(), name='doctor_register'),
]