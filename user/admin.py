from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CCUserCreationForm
from .models import CCUser
# Register your models here.

class CCUserAdmin(UserAdmin):
    form = CCUserCreationForm

admin.site.register(CCUser, CCUserAdmin)

