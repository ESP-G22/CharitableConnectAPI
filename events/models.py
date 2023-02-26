from django.db import models
from django.utils import timezone
import datetime

class Address(models.Model):
    lon = models.FloatField(blank=True) # Optional for Map Intergration
    lat = models.FloatField(blank=True)
    building_name = models.CharField(max_length = 50)
    street_name = models.CharField(max_length = 100)
    town_city = models.CharField(max_length = 100)
    postcode = models.CharField(max_length = 10)

class Event(models.Model):
    type = models.IntegerField(default = 0)
    title = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500)
    pub_date = models.DateTimeField('date published')
    date = models.DateTimeField('date of event')
    attendee_count = models.IntegerField(default = 0)
    organiser = models.CharField(max_length = 100)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    #Image
    #rsvp

    #Makes events easily identifiable in admin viewer.
    def __str__(self):
        return self.title
