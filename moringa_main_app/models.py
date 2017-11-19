from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Students(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    program = models.CharField(max_length=100)
    cohort = models.CharField(max_length=100)
    location = models.CharField(max_length=100)


class GlobalAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class LocalAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    program = models.CharField(max_length=100)


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    tardy = models.BooleanField()
    absent = models.BooleanField()
    excuse = models.CharField(max_length=1000)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    
    if created:
        LocalAdmin.objects.create(user=instance)
        Students.objects.create(user=instance)
        GlobalAdmin.objects.create(user=instance)
        if instance.students.program is not None and instance.students.program!="":
            instance.localadmin.delete()
            instance.globaladmin.delete()
        elif instance.localadmin.program is not None and instance.localadmin.program!="":
            instance.students.delete()
            instance.globaladmin.delete()
        else:
            instance.students.delete()
            instance.localadmin.delete()
    try:
        if instance.localadmin.program is not None and instance.localadmin.program != "":
            instance.localadmin.save()
            try:
                instance.globaladmin.delete()
            except:
                print()
        elif instance.students.program is not None and instance.students.program != "":
            instance.students.save()
            try:
                instance.globaladmin.delete()
            except:
                print()
        elif instance.globaladmin.id is not None:
            instance.globaladmin.save()
    except: print()




