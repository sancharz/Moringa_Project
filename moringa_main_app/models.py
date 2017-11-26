from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

#Choices

#Cohort
#The first element in each tuple is the actual value to be set on the model, 
#the second element is the human-readable name
COHORT_CHOICES = (
('1', 'COHORT 1'),
('2', 'COHORT 2'),
('3', 'COHORT 3'),
('4', 'COHORT 4'),
('5', 'COHORT 5'),
)

#Program
PROGRAM_CHOICES = (
('prep', "MORINGA PREP"),
('core', 'MORINGA CORE'),
)

#Can add more locations
#Location
LOCATION_CHOICES = (
('nairobi', "NAIROBI, KENYA"),
('mumbai', 'MUMBAI, INDIA'),
)

class Students(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    program = models.CharField(max_length = 10, choices = PROGRAM_CHOICES ) #changed the arguments here
    cohort = models.CharField(max_length = 1, choices = COHORT_CHOICES)#changed the arguments here
    location = models.CharField(max_length = 20, choices = LOCATION_CHOICES)#changed the arguments here


class GlobalAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class LocalAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=20, choices = LOCATION_CHOICES)#changed the arguments here
    program = models.CharField(max_length=10, choices = PROGRAM_CHOICES)#changed the arguments here


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




