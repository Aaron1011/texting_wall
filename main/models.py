from django.db import models
from django.contrib.auth.models import User
import string, random
# Create your models here.
def _generate_default_hashtag():
    return "".join(random.choice(string.lowercase) for i in range(3))
class Wall(models.Model):
    hashtag = models.CharField(max_length=20, help_text='Twitter hashtag to tweet to', default=_generate_default_hashtag())
    user =  models.ForeignKey(User, editable=False)

    def __unicode__(self):
        return self.name
        
TRAFFIC_SOURCE = (
    ('BG', 'Blog'),
    ('FR', 'Friend'),
    ('OT', 'Other',)
)
