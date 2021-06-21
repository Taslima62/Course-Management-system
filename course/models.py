from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from enum import Enum
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import math

class GetDateTime(object):
     
    def whenpublished(self):
        now = timezone.now()
        
        diff= now - self.time

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"              

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"
            elif days == 2:
                return str(days) + " days ago"
            else:
                return self.time
                
        return self.time #.strftime('%B %d, %Y')
class UserType(Enum):
    Student = 'Student',
    TA = 'TA',
    Teacher = 'Teacher',
    Admin = 'Admin'



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20,  choices=[('Student', _('Student')),('TA', _('TA')),
                                                          ('Teacher', _('Teacher')),('Admin', _('Admin'))],)
    address = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    registration = models.CharField(max_length=100, blank=True, help_text="Please your registration number if you are a student.")
    profile_image = models.ImageField(upload_to='course/images/', blank=True)

    def __str__(self):
        return self.user.username



class Contact(models.Model):
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=300)
    email = models.EmailField(max_length=111, default="")
    phone = models.CharField(max_length=12, default="")

    def __str__(self):
        return self.name


class Class(models.Model):
    course_code = models.CharField(max_length=111, default="")
    course_title = models.CharField(max_length=111, default="")
    course_credit = models.FloatField(default=0.0)
    section = models.CharField(max_length=111, default="")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, default="", unique=True)

    def __str__(self):
        return self.course_title

class Student_class(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    marks = models.FloatField(default=0.0)
    point = models.IntegerField(default=0) 
    answered_ques = models.IntegerField(default=0)
    asked_ques = models.IntegerField(default=0)
    join_date = models.DateTimeField(default=datetime.now, blank=True)
    course_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    



class Question_status(Enum):
    Pending = "Pending",
    Approved = 'Approved'


class Questions(models.Model, GetDateTime):
    course = models.ForeignKey(Class, on_delete=models.CASCADE)
    question = models.CharField(max_length=500, default="")
    asked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add= True)
    marks = models.FloatField(default=0.0)
    status = models.CharField(max_length=20,  choices=[('Pending', _('Pending')),('Approved', _('Approved'))],)

   

class Answers(models.Model, GetDateTime):
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.CharField(max_length=2000, default="")
    time = models.DateTimeField(auto_now_add= True)
    marks = models.FloatField(default=0.0) 
    status = models.CharField(max_length=20,  default="")
    vote = models.IntegerField(default=0) 



class VoteForAnswer(models.Model):
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.BooleanField (default=True)

class Short_question(models.Model, GetDateTime):
    course = models.ForeignKey(Class, on_delete=models.CASCADE)
    question = models.CharField(max_length=500, default="")
    asked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add= True)
    answer = models.CharField(max_length=100, default="")
    status = models.CharField(max_length=20,  choices=[('Pending', _('Pending')),('Approved', _('Approved'))],)

class Short_answered_by(models.Model, GetDateTime):
    question = models.ForeignKey(Short_question, on_delete=models.CASCADE)
    answered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add= True)
    answer = models.CharField(max_length=100, default="")