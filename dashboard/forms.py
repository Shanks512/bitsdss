from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
	username = forms.CharField(widget=TextInput)
	password = forms.CharField(widget=PasswordInput)
    class Meta:
        model = User 
        fields = ('username', 'password')
