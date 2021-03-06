from django.db import models
from django.contrib.auth.models import User
import string
import random


def _generate_default_hashtag():
    return "".join(random.choice(string.lowercase) for i in range(3))


class Wall(models.Model):
    hashtag = models.CharField(max_length=20, help_text='Twitter hashtag to tweet to', default=_generate_default_hashtag())
    user = models.ForeignKey(User, editable=False)
    phone_number = models.CharField(max_length=20)
    last_ping = models.DateTimeField(auto_now_add=True)
    top_prompt_text = models.CharField(max_length=1024, null=True, blank=True)
    bottom_prompt_text = models.CharField(max_length=1024, null=True, blank=True)

    def __unicode__(self):
        return self.hashtag


class MessageSender(models.Model):
    phone_number = models.CharField(max_length=20, null=True)
    twitter_username = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to="photos", null=True)
    fb_uid = models.IntegerField(null=True)

    def __unicode__(self):
        return self.name


class Message(models.Model):
    message = models.CharField(max_length=1024)
    time_sent = models.DateTimeField(auto_now_add=True)
    twitter_account = models.CharField(max_length=20, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    wall = models.ForeignKey(Wall)
    sender = models.ForeignKey(MessageSender, null=True)

    def __unicode__(self):
        return self.message


TRAFFIC_SOURCE = (
    ('BG', 'Blog'),
    ('FR', 'Friend'),
    ('OT', 'Other',)
)
