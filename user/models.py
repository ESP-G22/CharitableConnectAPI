from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy

class UserType(models.TextChoices):
    ORGANISER = 'ORGANISER', gettext_lazy('ORGANISER')
    USER = 'USER', gettext_lazy('USER')

class EventPreferences(models.TextChoices):
    TYPE1 = 'T1', gettext_lazy('Type1'),
    TYPE2 = 'T2', gettext_lazy('Type2'),
    TYPE3 = 'T3', gettext_lazy('Type3')

class CCUserManager(UserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError("User does not contain valid email")
        if not username:
            raise ValueError("User does not contain valid username")
        if not password:
            raise ValueError("User does not contain valid password")

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user



class CCUser(AbstractUser):
    eventPreferences = models.CharField(
        max_length=2,
        choices=EventPreferences.choices,
        default=EventPreferences.TYPE1
    )
    objects = CCUserManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    @property
    def is_organiser(self):
        return self.profile.userType == UserType.ORGANISER
    
    @property
    def is_user(self):
        return self.profile.userType == UserType.USER

class CCUserProfile(models.Model):
    user = models.OneToOneField(CCUser, on_delete=models.CASCADE, related_name="profile")
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=20, blank=True)
    dateJoined = models.DateTimeField(auto_now_add=True)
    userType = models.TextField(choices=UserType.choices, default=UserType.USER)
    followedUsers = models.ManyToManyField('self', related_name='followers', symmetrical=False,blank=True)
    twitter = models.URLField(default='', null=True,blank=True)
    website = models.URLField(default='', null=True,blank=True)
    instagram = models.URLField(default='', null=True,blank=True)
    facebook = models.URLField(default='',null=True,blank=True)
    avatar = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.username


    