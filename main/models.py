from django.db import models
from django.contrib.auth.models import User
import string, random
from django import forms
# Create your models here.
def _generate_default_hashtag():
    return "".join(random.choice(string.lowercase) for i in range(3))
class Wall(models.Model):
    hashtag = models.CharField(max_length=20, help_text='Twitter hashtag to tweet to', default=_generate_default_hashtag())
    user =  models.ForeignKey(User, editable=False)
    phone_number = models.CharField(max_length=20)
    def __unicode__(self):
        return self.hashtag

class Message(models.Model):
    message = models.CharField(max_length=1024)
    time_sent = models.DateTimeField(auto_now_add=True)
    twitter_account = models.CharField(max_length=20, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    wall = models.ForeignKey(Wall)


TRAFFIC_SOURCE = (
    ('BG', 'Blog'),
    ('FR', 'Friend'),
    ('OT', 'Other',)
)


