from django.db import models
import requests
from phe import paillier
from rest_framework.serializers import ModelSerializer
# Create your views here.


# Create your models here.
class EncryptedBMI(models.Model):
    email = models.CharField(max_length=200)
    underweight = models.TextField()
    normal = models.TextField()
    overweight = models.TextField()
    obese = models.TextField()

class EncryptedBMISerializer(ModelSerializer):
    class Meta:
        fields = ("email","underweight","normal","overweight","obese")
        model = EncryptedBMI

def aggregate_bmi():
    objects = EncryptedBMI.objects.all()
    categories = ["underweight","normal","overweight","obese"]
    public_key = requests.get('https://dev.medblocks.org/api/capsule/publicKey/').json()
    public_key = paillier.PaillierPublicKey(int(public_key['n']))
    aggregated = {}
    for c in categories:
        aggregated[c] = str(sum([paillier.EncryptedNumber(public_key, int(i.__dict__[c])) for i in objects]).ciphertext())
    data = {
        'count': len(objects),
        'data': aggregated
    }
    return requests.post(
        'https://dev.medblocks.org/api/capsule/decrypt/',
        json=data
    ).json()
