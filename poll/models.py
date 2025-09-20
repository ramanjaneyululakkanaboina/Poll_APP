from django.db import models
#from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateField('date published')
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.question_text
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True,blank=True)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text 

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student')
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.username} ({self.role})"