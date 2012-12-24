from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from main.models import Wall, Message
from django.conf import settings
import datetime
from django.utils.timezone import utc


@dajaxice_register
def verify_sms(request, message_id, areacode, first, second):
    try:
        message = Message.objects.get(pk=message_id)
    except Message.DoesNotExist:
        return simplejson.dumps({'status': False})

    if message.phone_number == "+1" + areacode + first + second:
        return simplejson.dumps({'status': True})

    return simplejson.dumps({'status': False})


@dajaxice_register
def close_wall(request, id):
    wall = Wall.objects.get(pk=id)
    print "Closing wall"
    wall.last_ping -= datetime.timedelta(minutes=settings.WALL_EXPIRATION)
    print wall.last_ping
    wall.save()


@dajaxice_register
def ping_wall(request, id):
    wall = Wall.objects.get(pk=id)
    wall.lastping = datetime.datetime.utcnow().replace(tzinfo=utc)
    print wall.lastping
    wall.save()
