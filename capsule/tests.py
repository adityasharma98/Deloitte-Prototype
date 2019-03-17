from django.test import TestCase
from .encryption import generate_key_pair
from django.core.exceptions import ValidationError
from .models import PublicKey, PrivateKey
import random
from rest_framework.test import APIClient
from capsule import views
import json
from phe import paillier
# Create your tests here.
class TestKey(TestCase):
    def setUp(self):
        public, private = generate_key_pair()
    
    def test_key_exists(self):
        public = PublicKey.objects.first()
        private = PrivateKey.objects.first()
        self.assertEqual(private.public_key, public)

    def test_key_add(self):
        try:
            generate_key_pair()
            self.assertTrue(False)
        except ValidationError as e:
            self.assertTrue(True)
        
        self.assertEqual(1, len(PublicKey.objects.all()))

    def test_encryption(self):
        public = PublicKey.objects.first()
        public = public.public_key()
        private = PrivateKey.objects.first()
        private = private.private_key()
        ans = public.encrypt(5) + public.encrypt(4)
        self.assertEqual(private.decrypt(ans), 5+4)

class TestBMI(TestCase):
    def setUp(self):
        public, private = generate_key_pair()
    
    def test_random_bmi_aggregation(self):
        # Initialize client
        api = APIClient()
        # Get Public Key
        response = api.get('/api/capsule/publicKey/')
        print(response.content)
        # Load JSON and make public key object
        public_key = json.loads(response.content.decode())
        public_key = paillier.PaillierPublicKey(int(public_key['n']))
        # BMI Categories
        categories = ['underweight','normal','overweight','obese']
        count = 30
        # Generate random data
        data = {c:public_key.encrypt(0) for c in categories}
        for i in range(count):
            data[random.choice(categories)] += public_key.encrypt(1)
        data = {k:str(data[k].ciphertext()) for k in data.keys()}
        
        # Aggregated data to decrypt
        aggregated = {
            'data':data,
            'count': count
        }
        # Truncate for printing
        fmt_data = {k:data[k][:75]+'...' for k in data.keys()}
        fmt_aggregated = {
            'data': fmt_data,
            'count': count
        }
        print("Encrypted request: \n{}".format(aggregated))

        # Decrypt API
        response = api.post('/api/capsule/decrypt/',aggregated, format='json')
        print("Decrypted result:\n{}".format(response.content))
        response = json.loads(response.content.decode())
        self.assertEqual(response['count'], sum(response['data'].values()))

