from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Course(models.Model):
    course_name = models.CharField(max_length=100, blank=False)
    units = models.IntegerField(default=3)
    description = models.TextField()
    is_current_sem = models.BooleanField(default=False)

class Section(models.Model):
    SECTION_TYPES = (
        ('LEC', 'Lecture'),
        ('TUT', 'Tutorial'),
        ('PRA', 'Practical'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_type = models.CharField(max_length=3, choices=SECTION_TYPES, blank=False)
    display_text = models.CharField(max_length=50, blank=False)
    num_hours = models.IntegerField(blank=False)

    class Meta:
        unique_together = ("course", "display_text")

class User(models.Model):
    ROLES = (
        ('ADM', 'Admin'),
        ('HOD', 'Head Of Department'),
        ('FAC', 'Faculty'),
    )
    user_name = models.CharField(max_length=100, blank=False)
    role = models.CharField(max_length=3, choices=ROLES, blank=False)
    password = models.CharField(max_length=100, blank=False)
    expert_courses = models.ManyToManyField(Course, through='Expertise', related_name='experts')
    prev_assigned_courses = models.ManyToManyField(Course, through='PrevAssignment', related_name='prev_assignees')
    applied_sections = models.ManyToManyField(Section, through='Application')

class TimeWindow(models.Model):
    name = models.CharField(max_length=100, blank=False)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)

class Tag(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=100)

class Expertise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    num_years = models.IntegerField(default=1)

    class Meta:
        unique_together = ("user", "course")

class PrevAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.IntegerField(default=2015)

    class Meta:
        unique_together = ("user", "course")

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    is_assigned = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "section")