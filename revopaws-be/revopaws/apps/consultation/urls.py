from django.urls import path
from .views import (
    ConsultationBookingView,
    ConsultationPaymentView,
    ConsultationStartView,
    ConsultationEndView,
    DoctorReviewCreateView,
    FileUploadView
)

urlpatterns = [
    path("consultations/upload-file/", FileUploadView.as_view(), name="file-upload"),
    path('consultations/book/', ConsultationBookingView.as_view(), name='consultation-booking'),
    path('consultations/<int:consultation_id>/payment/', ConsultationPaymentView.as_view(), name='consultation-payment'),
    path('consultations/<int:consultation_id>/start/', ConsultationStartView.as_view(), name='consultation-start'),
    path('consultations/<int:consultation_id>/end/', ConsultationEndView.as_view(), name='consultation-end'),
    path('consultations/<int:consultation_id>/review/', DoctorReviewCreateView.as_view(), name='consultation-review'),
]