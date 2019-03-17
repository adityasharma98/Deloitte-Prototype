from django.apps import AppConfig

from django.core.exceptions import ValidationError
from django.db.utils import OperationalError, ProgrammingError
class CapsuleConfig(AppConfig):
    name = 'capsule'
    verbose_name = "Homomorphic Encryption Capsule"
    def ready(self):
        from capsule.encryption import generate_key_pair
        from capsule.models import PublicKey, PrivateKey
        try:
            if PublicKey.objects.exists() and PrivateKey.objects.exists():
                print("Capsule service keys exist")
                return
            generate_key_pair()
        except OperationalError:
            print("Running migration...")
            return
        except ProgrammingError:
            print("Running migration...")
            return
        print("Generating Capsule service keys...")