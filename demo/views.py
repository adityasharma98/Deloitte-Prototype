from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView, Response
from .models import EncryptedBMISerializer, EncryptedBMI, aggregate_bmi
from django.views.generic import TemplateView

class Home(TemplateView):
    template_name = 'demo.html'

class EncryptedBMIView(ListCreateAPIView):
    queryset = EncryptedBMI.objects.all()
    serializer_class = EncryptedBMISerializer

class AggregateBMIView(APIView):
    def get(self, request):
        data = aggregate_bmi()
        return Response(data)