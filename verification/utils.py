import requests
from medblocks_oracle.settings import MAILGUN_DOMAIN, MAILGUN_API_KEY
from django.urls import reverse
def send_code(to, code, request):
    url = "{scheme}://{host}{path}".format(
        scheme=request.scheme, 
        host=request.get_host(),
        path=reverse('email-verify', kwargs={'email':to,'code':code})
        )
    return requests.post(
        "https://api.mailgun.net/v3/{}/messages".format(MAILGUN_DOMAIN),
        auth=("api", MAILGUN_API_KEY),
        data={
            "from":"Team MedBlocks <verification@medblocks.org>",
            "to": [to],
            "subject": "MedBlocks Verification",
            "text": "Click on this link to verify: {}".format(url)
        }
    )

