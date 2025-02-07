from django.urls import path
from .views import (
    UserLoginView, UserRegisterView,
    DoctorLoginView, DoctorRegisterView,
    UserProfileUpdateView, DoctorProfileUpdateView,
    ChangePasswordView
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('profile/', UserProfileUpdateView.as_view(), name='user_profile'),
    path('doctor/login/', DoctorLoginView.as_view(), name='doctor_login'),
    path('doctor/register/', DoctorRegisterView.as_view(), name='doctor_register'),
    path('doctor/profile/', DoctorProfileUpdateView.as_view(), name='doctor_profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('doctor/change-password/', ChangePasswordView.as_view(), name='doctor_change_password'),
]