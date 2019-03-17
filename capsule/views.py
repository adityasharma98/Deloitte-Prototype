from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PublicKey, PrivateKey, KeySerializer
from rest_framework.reverse import reverse, reverse_lazy
# Create your views here.
class ApiRootView(APIView):
    def get(self, request):
        return Response({
            'capsule': reverse('capsule-root', request=request),
            'verify': reverse('email-send', request=request)
            # 'verification': reverse('verification', request=request)
        })

class CapsuleAPIRootView(APIView):
    def get(self, request):
        return Response({
            'publicKey': reverse('publicKey', request=request),
            'decrypt': reverse('decrypt', request=request)
        })

class PublicKeyView(APIView):
    """
    GET: The n and g value of the Homomorphic public key. In this case, g = n+1
    """
    def get(self, request):
        public_key = KeySerializer(PublicKey.objects.first())
        return Response(public_key.data)

class DecryptView(APIView):
    """
    POST: Decrypts data after aggregation. Currently works with BMI categories. The count after decryption must be equal to the sum of the encrypted categories.
    Example post request
    {
        "data": {
            "underweight":23203482039480230948...,
            "normal":203948203481353434...,
            "overweight":09809834573942384234...
            },
        "count":23
    }
    Real data here: https://pastebin.com/DMAB4B8f for keys at https://pastebin.com/NuDth5qy

    """
    def post(self, request):
        private_key = PrivateKey.objects.first()
        data = request.data['data']
        count = request.data['count']
        decrypted = {}
        for category in data.keys():
            decrypted[category] = private_key.decrypt(int(data[category]))
        if count == sum(decrypted.values()):
            return Response({'data':decrypted, 'count':count})
        else:
            return Response({'error':'Aggregation does not equal count'})