from .models import CCUser, CCUserProfile
from django.db.models.signals import post_save, pre_migrate
from django.dispatch import receiver

@receiver(post_save, sender=CCUser)
def createCCUserProfile(sender, instance, created, **kwargs):
    if created:
        CCUserProfile.objects.create(user=instance)
        
