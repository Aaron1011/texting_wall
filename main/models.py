from django.db import models
from django.contrib.auth.models import User
import string, random
# Create your models here.

class Wall(models.Model):
    def get_hashtag():
        return "".join([random.choice(string.lowercase) for i in range(3)])
    sms_keyword = models.CharField(max_length=20, help_text=('Keyword to start messages with'))
    hashtag = models.CharField(max_length=20, help_text='Twitter hashtag to tweet to', default=get_hashtag())
    user =  models.ForeignKey(User, editable=True)

    def __unicode__(self):
        return self.name
        
TRAFFIC_SOURCE = (
    ('BG', 'Blog'),
    ('FR', 'Friend'),
    ('OT', 'Other',)
)
