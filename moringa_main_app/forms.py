from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import moringa_main_app.models 

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

#Can add more locatIONS
#Location
LOCATION_CHOICES = (
('nairobi', "NAIROBI, KENYA"),
('mumbai', 'MUMBAI, INDIA'),
)

#3 different types of users
USER_TYPES = (
('ga', 'GLOBAL ADMINSTRATOR'),	
('la', 'LOCAL ADMINSTRATOR'),
('st', 'STUDENT'), 
)

class SignUpForm(UserCreationForm):
    #added the emailfield below to ensure username is an email
    username = forms.EmailField(max_length = 254, required = True)
    first_name = forms.CharField(max_length = 30, required = True)
    last_name = forms.CharField(max_length = 30, required = True)
    #changed the arguments so it reflects the distinct choices available - sancharz
    user_type = forms.ChoiceField(choices = USER_TYPES, required = True) #la, ga, st
    program = forms.ChoiceField( choices = PROGRAM_CHOICES, required = True)
    cohort = forms.ChoiceField( choices = COHORT_CHOICES, required = False) #local admins do not have to specify cohort
    location = forms.ChoiceField(choices = LOCATION_CHOICES,  required = True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )
