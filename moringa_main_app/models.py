from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Students(models.Model):
    userId = models.OneToOneField(User, on_delete=models.CASCADE)
    program = models.CharField(max_length=100)
    cohort = models.CharField(max_length=100)
    location = models.CharField(max_length=100)


class GlobalAdmin(models.Model):
    userId = models.OneToOneField(User, on_delete=models.CASCADE)


class LocalAdmin(models.Model):
    userId = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    program = models.CharField(max_length=100)


class Attendance(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    tardy = models.BooleanField()
    absent = models.BooleanField()
    excuse = models.CharField(max_length=1000)


    




