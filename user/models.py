from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy


class SocialLinks(models.Model):
    twitter = models.URLField(default='')
    website = models.URLField(default='')
    instagram = models.URLField(default='')
    facebook = models.URLField(default='')

class UserType(models.TextChoices):
    SITEADMIN = 'S_ADMIN', gettext_lazy('SiteAdmin')
    ORGNAISER = 'ORGNAISER', gettext_lazy('ORGNAISER')
    USER = 'USER', gettext_lazy('USER')

class EventPreferences(models.TextChoices):
    TYPE1 = 'T1', gettext_lazy('Type1'),
    TYPE2 = 'T2', gettext_lazy('Type2'),
    TYPE3 = 'T3', gettext_lazy('Type3')

class CCUserManager(UserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError("User does not contain valid email")
        user = self.model(
            email=self.normalize_email(email),
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class CCUser(AbstractUser):
    socialLinks = models.OneToOneField(SocialLinks, on_delete=models.CASCADE, null=True)
    bio = models.TextField()
    profilePic = models.ImageField()
    eventPreferences = models.CharField(
        max_length=2,
        choices=EventPreferences.choices,
        default=EventPreferences.TYPE1
    )
    userType = models.TextField(choices=UserType.choices, default=UserType.USER)
    followedUsers = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    objects = CCUserManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    @property
    def is_orgnaiser(self):
        return self.userType == UserType.ORGNAISER
    
    @property
    def is_user(self):
        return self.userType == UserType.USER



    