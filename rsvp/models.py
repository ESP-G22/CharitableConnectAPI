from django.db import models
from user.models import CCUser
from events.models import Event

class RSVP(models.Model):
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE)
    user = models.ForeignKey(to=CCUser, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(auto_now_add=True)