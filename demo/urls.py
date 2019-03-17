from django.urls import path
from demo.views import Home, EncryptedBMIView, AggregateBMIView

urlpatterns = [
    path('', Home.as_view()),
    path('bmi/',EncryptedBMIView.as_view()),
    path('aggregate/', AggregateBMIView.as_view())
]