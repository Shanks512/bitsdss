from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

# Create your models here.

@python_2_unicode_compatible
class Course(models.Model):
    course_name = models.CharField(max_length=100, blank=False)
    course_code = models.CharField(max_length=10, default="CS101")
    units = models.IntegerField(default=3)
    description = models.TextField()
    is_current_sem = models.BooleanField(default=False)

    experts = models.ManyToManyField(User, through='Expertise', related_name='expert_courses')
    prev_assignees = models.ManyToManyField(User, through='PrevAssignment', related_name='prev_assigned_courses')

    def __str__(self):
        return self.course_name

@python_2_unicode_compatible
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

    applied_users = models.ManyToManyField(User, through='Application')

    class Meta:
        unique_together = ("course", "display_text")

    def __str__(self):
        return (self.course.course_name + " " + self.section_type + " " + self.display_text)

@python_2_unicode_compatible
class TimeWindow(models.Model):
    name = models.CharField(max_length=100, blank=False)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Tag(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return self.tag_name

@python_2_unicode_compatible
class Expertise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    num_years = models.IntegerField(default=1)

    class Meta:
        unique_together = ("user", "course")
    
    def __str__(self):
        return (self.user.username + "_" + self.course.course_name + "_" + str(self.num_years) + "_years")

@python_2_unicode_compatible
class PrevAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.IntegerField(default=2015)

    class Meta:
        unique_together = ("user", "course")
    
    def __str__(self):
        return (self.user.username + "_" + self.course.course_name + "_" + str(self.year))

@python_2_unicode_compatible
class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    is_assigned = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "section")

    def __str__(self):
        return (self.user.username + "_" + self.section.__str__())        