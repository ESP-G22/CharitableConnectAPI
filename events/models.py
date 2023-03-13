from django.db import models
from user.models import CCUser
from django.utils import timezone
import datetime

class Event(models.Model):
    type = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    pubDate = models.DateTimeField('date published', auto_now_add=True)
    date = models.DateTimeField('date of event')
    organiser = models.ForeignKey(CCUser, on_delete=models.CASCADE)
    address1 = models.TextField(max_length=200)
    address2 = models.TextField(max_length=200, null=True)
    postcode = models.TextField(max_length=10)

    # aceess RSVP using event.rsvp_set
    #Image

    @property
    def attendeeCount(self):
        return len(self.rsvp_set.all())

    #Makes events easily identifiable in admin viewer.
    def __str__(self):
        return self.title
