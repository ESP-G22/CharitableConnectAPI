from rest_framework import serializers
from .models import *
from user.serializers import CCUserProfileSerializer
from rsvp.models import RSVP
from rsvp.serializer import CCRSVPSerializer
class CCEventSerializer(serializers.ModelSerializer):
    organiser = CCUserProfileSerializer(read_only=True)
    attendeeCount = serializers.IntegerField()
    rsvp = serializers.SerializerMethodField(method_name='check_rsvp')

    def check_rsvp(self, event):
        if 'user_id' in self.context:
            rsvp = event.rsvp_set.filter(user=self.context['user_id'])
            if rsvp.exists():
                return CCRSVPSerializer(rsvp[0]).data
        return None

    class Meta:
        model = Event
        fields = '__all__'

class CCNewEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['organiser']

class CCEventSearchSerializer(serializers.Serializer):
    searchTerm = serializers.CharField()
