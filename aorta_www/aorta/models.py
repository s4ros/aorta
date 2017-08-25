from django.db import models
from django.utils import timezone

# Create your models here.


class Chatter(models.Model):
    nick = models.CharField(max_length=100)
    popularity = models.IntegerField(default=0)
    money = models.IntegerField(default=0)
    last_seen = models.DateField(default=timezone.now)
    time_spent = models.IntegerField(default=0)
    is_following = models.BooleanField(default=False)
    is_subscribing = models.BooleanField(default=False)


class Logs(models.Model):
    nick = models.ForeignKey(Chatter, related_name='chatter')
    date = models.DateField(default=timezone.now)
    text = models.CharField(max_length=350)
