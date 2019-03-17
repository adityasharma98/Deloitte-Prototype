from django.urls import path
from verification.views import VerifyEmailView, SendEmailView, RegistrationDetailView

urlpatterns = [
    path('',SendEmailView.as_view(), name='email-send'),
    path('<str:email>/<str:code>', VerifyEmailView.as_view(), name='email-verify'),
    path('<str:email>/', RegistrationDetailView.as_view(), name='registration-detail'),
]