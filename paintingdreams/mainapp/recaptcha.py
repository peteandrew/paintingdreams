import requests

from django.conf import settings

def check_recaptcha(request):
    recaptcha_response = request.POST.get('g-recaptcha-response')
    ''' Begin reCAPTCHA validation '''
    data = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()
    ''' End reCAPTCHA validation '''
    return result['success']
