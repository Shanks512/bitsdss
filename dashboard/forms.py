from django import forms
from django.forms import DateTimeField
from django.contrib.auth.models import User
from .models import *

CHOICES = [('faculty','Faculty'),('hod', 'Head of Department')]

course_list = Course.objects.all()

class RegisterForm(forms.ModelForm):
    firstname = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Full Name', 'class':'form-control'}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name', 'class':'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username', 'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password here', 'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Retype password', 'class':'form-control'}))
    designation = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    course_name = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    exp_years = forms.CharField(widget=forms.NumberInput(attrs={'placeholder':'Years of Experience', 'class':'form-control'}))
    class Meta:
        model = User 
        fields = ('firstname', 'lastname', 'username', 'designation', 'password', 'password2', 'course_name', 'exp_years')

class EditProfile(forms.ModelForm):
    firstname = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Full Name', 'class':'form-control'}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name', 'class':'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username', 'class':'form-control'}))
    designation = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    course_name = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    exp_years = forms.CharField(widget=forms.NumberInput(attrs={'placeholder':'Years of Experience', 'class':'form-control'}))
    class Meta:
        model = User 
        fields = ('firstname', 'lastname', 'username', 'designation', 'course_name', 'exp_years')

class AddCourseForm(forms.ModelForm):
    course_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Course name', 'class':'form-control'}))
    course_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Course code', 'class':'form-control'}))
    units = forms.CharField(widget=forms.NumberInput(attrs={'placeholder':'Number of units', 'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':8,'placeholder':'Course description', 'style':'width:100%;margin-top:30px;'}))

    class Meta:
        model = Course
        fields = ('course_name', 'course_code', 'units', 'description')

class SetWindowsForm(forms.ModelForm):
    course_selection_start = forms.DateField(widget=forms.DateInput(attrs={'placeholder':'Start date', 'id':'datetimepicker1', 'class':'form-control date-picker'}),)
    course_selection_end = forms.DateField(widget=forms.TextInput(attrs={'placeholder':'End date', 'id':'datetimepicker2', 'class':'form-control'}),)

    course_application_start = forms.DateField(widget=forms.TextInput(attrs={'placeholder':'Start date', 'id':'datetimepicker3', 'class':'form-control'}),)
    course_application_end = forms.DateField(widget=forms.TextInput(attrs={'placeholder':'End date', 'id':'datetimepicker4', 'class':'form-control'}),)

    course_assignment_start = forms.DateField(widget=forms.TextInput(attrs={'placeholder':'Start date', 'id':'datetimepicker5', 'class':'form-control'}),)
    course_assignment_end = forms.DateField(widget=forms.TextInput(attrs={'placeholder':'End date', 'id':'datetimepicker6', 'class':'form-control'}),)

    class Meta:
        model = TimeWindow
        fields = ('course_selection_start', 'course_selection_end', 'course_application_start', 
            'course_application_end', 'course_assignment_start', 'course_assignment_end')