from django.db import models
from user.models import CCUser
from django.utils.translation import gettext_lazy
import json
import uuid
from django.utils import timezone
import datetime

# Event types:Local Business, Climate, Community, Sports, Other.

class EventType(models.TextChoices):
    LocalBusiness = 'LocalBusiness', gettext_lazy('Local Business')
    Climate = 'Climate', gettext_lazy('Climate')
    Community = 'Community', gettext_lazy('Community')
    Sports = 'Sports', gettext_lazy('Sports')
    Other = 'Other', gettext_lazy('Other')


class Event(models.Model):
    type = models.CharField(choices=EventType.choices, default=EventType.Other,max_length=20)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    pubDate = models.DateTimeField('date published', auto_now_add=True)
    date = models.DateTimeField('date of event')
    organiser = models.ForeignKey(CCUser, on_delete=models.CASCADE)
    address1 = models.TextField(max_length=200)
    address2 = models.TextField(max_length=200, null=True)
    postcode = models.TextField(max_length=10)
    images = models.JSONField(default=list)

    @staticmethod
    def validate_images_json(j):
        if 'images' not in j: return True
        try:
            obj = j['images']
            if type(obj) != list:
                return False
            else:
                for s in obj:
                    uuid.UUID(s)
        except Exception as e:
            print(e)
            return False
        return True

    @property
    def attendeeCount(self):
        return len(self.rsvp_set.all())

    #Makes events easily identifiable in admin viewer.
    def __str__(self):
        return self.title
