from phe import paillier
from .models import PublicKey, PrivateKey

def generate_key_pair():
    public, private = paillier.generate_paillier_keypair()
    public = PublicKey.objects.create(n=public.n, g=public.g)
    private = PrivateKey.objects.create(p=private.p, q=private.q, public_key=public)
    return public, private