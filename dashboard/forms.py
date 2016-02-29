from django import forms
from django.contrib.auth.models import User
from .models import *

CHOICES = [('faculty','Faculty'),('hod', 'Head of Department')]

class RegisterForm(forms.ModelForm):
    firstname = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Full Name', 'class':'form-control'}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name', 'class':'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username', 'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password here', 'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Retype password', 'class':'form-control'}))
    designation = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = User 
        fields = ('firstname', 'lastname', 'username', 'designation', 'password', 'password2',)

class AddCourseForm(forms.ModelForm):
    course_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Course name', 'class':'form-control'}))
    course_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Course code', 'class':'form-control'}))
    units = forms.CharField(widget=forms.NumberInput(attrs={'placeholder':'Number of units', 'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':8,'placeholder':'Course description', 'style':'width:100%;margin-top:30px;'}))

    class Meta:
        model = Course
        fields = ('course_name', 'course_code', 'units', 'description') 