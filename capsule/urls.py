from django.urls import path
from .views import PublicKeyView, DecryptView, CapsuleAPIRootView

urlpatterns = [
    path('',CapsuleAPIRootView.as_view(), name='capsule-root'),
    path('publicKey/', PublicKeyView.as_view(), name='publicKey'),
    path('decrypt/', DecryptView.as_view(), name='decrypt')
]