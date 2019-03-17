
 - Capsule service for Aggregated Homomorphic Encryption

## Installation
Install dependencies and run migrations

```
virtualenv venv
pip install -r requirements.txt
python manage.py migrate
```

Run tests

```
python manage.py test
```
Run this while running the server on http://localhost:8000 to test with the real database keys.
You will need to install the extra depndencies (requests) yourself.
```
pip install requests
python test_real_db.py
```

Run server

```
python manage.py runserver
```


## Usage
### Capsule services
Self documented endpoints
- GET /api/capsule/publicKey
- POST /api/capsule/decrypt

### Email services
- POST /api/verify/
- GET /api/verify/email@example.com/verification-code