from django.db import models
from django.core.exceptions import ValidationError
from rest_framework import serializers
from phe import paillier
# Create your models here.
class PublicKey(models.Model):
    n = models.CharField(max_length=617)
    g = models.CharField(max_length=617)

    def public_key(self):
        return paillier.PaillierPublicKey(n=int(self.n))

    def save(self, *args, **kwargs):
        if PublicKey.objects.exists() and not self.pk:
            raise ValidationError('There is can be only one PublicKey instance')
        return super(PublicKey, self).save(*args, **kwargs)

class PrivateKey(models.Model):
    p = models.CharField(max_length=309)
    q = models.CharField(max_length=309)
    public_key = models.ForeignKey(PublicKey, models.CASCADE, 'private_key')

    def private_key(self):
        return paillier.PaillierPrivateKey(p=int(self.p), q=int(self.q), public_key=self.public_key.public_key())

    def save(self, *args, **kwargs):
        if PrivateKey.objects.exists() and not self.pk:
            raise ValidationError('There is can be only one PrivateKey instance')
        return super(PrivateKey, self).save(*args, **kwargs)
    
    def decrypt(self, number):
        public_key = self.public_key.public_key()
        private_key = self.private_key()
        encrypted_number = paillier.EncryptedNumber(public_key, number)
        return private_key.decrypt(encrypted_number)

class KeySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('n','g')
        read_only_fields = ('n','g')
        model = PublicKey
