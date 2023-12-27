from django.db import models
from django.contrib.auth.models import User
from datetime import date

class todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    complete = models.BooleanField(default=False)
    end_date = models.DateField()

    def __str__(self):
        return self.title
    

class task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, null=True)
    start_time = models.TimeField(default=None, null=True)
    start_date = models.DateField(default=None)
    end_time = models.TimeField(default=None, null=True)
    end_date = models.DateField(default=None)
    repeat = models.CharField(max_length=20, choices=[
        ('none', 'None'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ], default='none')
    all_day = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    