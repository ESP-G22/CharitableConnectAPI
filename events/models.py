from django.db import models
from user.models import CCUser
from django.utils import timezone
import datetime

class Address(models.Model):
    lon = models.FloatField(blank=True, null=True) # Optional for Map Intergration
    lat = models.FloatField(blank=True, null=True)
    buildingName = models.CharField(max_length = 50)
    streetName = models.CharField(max_length = 100)
    townCity = models.CharField(max_length = 100)
    postcode = models.CharField(max_length = 10)

class Event(models.Model):
    type = models.IntegerField(default = 0)
    title = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500)
    pubDate = models.DateTimeField('date published', auto_now_add=True)
    date = models.DateTimeField('date of event')
    organiser = models.ForeignKey(CCUser, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, blank=True, null=True)

    #Image
    #rsvp

    @property
    def attendeeCount(self):
        return 0 # Todo generate from rsvp

    #Makes events easily identifiable in admin viewer.
    def __str__(self):
        return self.title
