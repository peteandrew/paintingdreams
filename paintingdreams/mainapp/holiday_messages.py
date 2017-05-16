import datetime
import pytz
from mainapp.models import HolidayMessage

def messages():
    message_objects = HolidayMessage.objects.filter(start__lte=datetime.datetime.now(tz=pytz.utc)).filter(end__gt=datetime.datetime.now(tz=pytz.utc))

    messages = {}
    for message_object in message_objects:
        if message_object.website_message:
            messages['website'] = message_object.website_message
        if message_object.email_message:
            messages['email'] = message_object.email_message
        if message_object.wholesale_message:
            messages['wholesale'] = message_object.wholesale_message

    return messages
