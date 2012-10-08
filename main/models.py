from django.db import models

# Create your models here.

class Wall(models.Model):
    name = models.CharField(max_length=20)
    hashtag = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name
