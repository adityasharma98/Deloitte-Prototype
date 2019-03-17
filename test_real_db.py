import requests
from phe import paillier
import random
def test_real_db():
    public_key = requests.get('http://localhost:8000/api/capsule/publicKey/').json()
    public_key = paillier.PaillierPublicKey(int(public_key['n']))
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
    r = requests.post('http://localhost:8000/api/capsule/decrypt/', json=aggregated)
    print(r.json())

if __name__ == '__main__':
    test_real_db()

