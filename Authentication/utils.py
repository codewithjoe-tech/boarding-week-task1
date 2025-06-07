from django.core import signing
from django.conf import settings



def create_signed_url(email : str):
    value = signing.dumps(email , salt='email-verification')
    
    url = settings.FRONTEND_URL
    return f"{url}/auth/verify/{value}"


