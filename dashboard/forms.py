from django import forms
from django.contrib.auth.models import User
from .models import *

'''class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=TextInput)
    password = forms.CharField(widget=PasswordInput)
    class Meta:
        model = User 
        fields = ('username', 'password') '''

class AddCourseForm(forms.ModelForm):
    course_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Course name', 'class':'form-control'}))
    course_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Course code', 'class':'form-control'}))
    units = forms.CharField(widget=forms.NumberInput(attrs={'placeholder':'Number of units', 'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':8,'placeholder':'Course description', 'style':'width:100%;margin-top:30px;'}))

    class Meta:
        model = Course
        fields = ('course_name', 'course_code', 'units', 'description') 