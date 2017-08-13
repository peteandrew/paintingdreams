import requests
import json
import logging

from django.conf import settings

logger = logging.getLogger('django')

def mailchimp_subscribe(subscriber):
    data = {
        "email_address": subscriber['email'],
        "email_type": "html",
        "status": "subscribed",
        "merge_fields": {
            "FNAME": subscriber['first_name'],
            "LNAME": subscriber['last_name']
        }
    }
    r = requests.post('https://us1.api.mailchimp.com/3.0/lists/a4cdc2ecc7/members', data=json.dumps(data), auth=('blank', settings.MAILCHIMP_APIKEY))
    result = r.json()

    if result['status'] != 200 and 'title' in result and result['title'] != 'Member Exists':
        logger.debug(result)
        return False

    return True
