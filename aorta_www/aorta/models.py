from django.db import models
from django.utils import timezone

# Create your models here.


class Chatter(models.Model):
    nick = models.CharField(max_length=100, unique=True)
    popularity = models.IntegerField(default=0)
    money = models.IntegerField(default=0)
    last_seen = models.DateTimeField(default=timezone.now)
    time_spent = models.IntegerField(default=0)
    is_following = models.BooleanField(default=False)
    is_subscribing = models.BooleanField(default=False)

    def __str__(self):
        return "{}. {}".format(self.id, self.nick)


class Log(models.Model):
    nick = models.ForeignKey(Chatter, related_name='logs')
    date = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=350)
