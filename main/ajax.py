from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from main.models import Message, MessageSender

@dajaxice_register
def verify_sms(request, message_id, areacode, first, second):
    print "Function started"
    try:
        message = Message.objects.get(pk=message_id)
    except Message.DoesNotExist:
        return simplejson.dumps({'status':False})

    if message.phone_number == "+1" + areacode + first + second:
        return simplejson.dumps({'status':True})

    return simplejson.dumps({'status':False})
