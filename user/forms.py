from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CCUser

class CCUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='password')

    class Meta:
        model = CCUser
        fields = ('email', 'username')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.password)
        if commit: user.save()
        return user
    
    