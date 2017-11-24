from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from moringa_main_app.forms import SignUpForm
from django.http import HttpResponseRedirect, HttpResponse
#for database queries 
from moringa_main_app.models import Attendance
from moringa_main_app.models import Students
from moringa_main_app.models import GlobalAdmin
from moringa_main_app.models import LocalAdmin

# for getting time
from datetime import datetime
# for getting ip address
from ipware.ip import get_ip

#MORINGA_IP_ADDRESS = '65.112.8.133' # emily h's ip address to test
MORINGA_IP_ADDRESS = '127.0.0.1' # sancharz's ip address to test


# developer admin page
def index(request):
    return render(request, 'student_view/index.html', None)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid(): # probably discard this
            user = form.save()
            user.refresh_from_db()
            if form.cleaned_data.get('user_type') == 'ga':
                user.save()
                return render(request, 'registration/signup.html', {'form': form})
            elif form.cleaned_data.get('user_type') == 'la':
                user.localadmin.program = form.cleaned_data.get('program')
                user.localadmin.location = form.cleaned_data.get('location')
                user.save()        
                return render(request, 'registration/signup.html', {'form': form})
            user.students.program = form.cleaned_data.get('program')
            user.students.location = form.cleaned_data.get('location')
            user.students.cohort = form.cleaned_data.get('cohort')
            #user.groups = form.cleaned_data.get('user_type')
            user.save()
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout(request):
    return render(request, 'logout.html')

# login
def login(request):
    if request.method == 'GET':
        print('gotem') #debugging
        return render(request, 'registration/login.html', None)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            #authentication passed so login the user
            auth_login(request, user)
            #query the database to determine the type of user - sancharz
            #assuming that the appropraite tables were 
            #**not too confident if my arguments are correct - sancharz
            query_s = Students.objects.filter(user = request.user)
            query_la = LocalAdmin.objects.filter(user = request.user)
            query_ga = GlobalAdmin.objects.filter(user = request.user)
            #redirect to a success page - sancharz
            #check if a query set is empty - sancharz
            if query_s:
                #user is a student 
                return redirect('/check_in/')
            if query_la:
                #user is a la
                return redirect('/view_record/')
            if query_ga:
                #user is a ga
                return redirect('/location_view/')

            #commented this code out to test if alternative works - sancharz
            # if hasattr(user, 'localadmin') is not None:
            #     return redirect('/check_in/')
            # elif hasattr(user, 'students'):
            #     return redirect('/view_record/')
            # else:
            #     return redirect('/location_view/')
        else:
            # Return an 'invalid login' error message. NOT DONE
            return redirect('/login/')
         

# check in for students
@login_required
def check_in(request):
    if request.method == 'GET':
        # make time_status && location_status 
        # time_status == 1 (on time); == 0 (late)
        # location_status == 1 (on campus); == 0 (not on campus)
        # check location
        message = "" # initialize a variable to hold a message based on student status
        status = "" # initialize a variable to hold a student status

        # get user's IP address --> https://github.com/un33k/django-ipware
        ip = get_ip(request)
        print("THIS IS THE IP ADDRESS FOLKS", end = "") #debugging
        print(ip) # debugging
        if not ip: # if IP address not retrieved (error check)
            print("we don't have an IP address for user")
        
        if ip == MORINGA_IP_ADDRESS: # on campus
            location_status = 1
        else: # not on campus
            location_status = 0
        
        if location_status == 0: # if not on campus, render absent page
            status = "Not on Campus"
            message = "You are not currently on campus. If applicable, please leave an excuse for your absence."
            return render(request, 'student_view/check_in.html', {'student_status':status, 'message': message})
        else: # only check time if student is on campus
            # check time
            if datetime.now().time() <= datetime.strptime('080000', '%H%M%S').time(): # on time
                time_status = 1
                status = "On Time"
                message = "you are on time. please submit your attendance!"
                return render(request, 'student_view/check_in.html', {'student_status':status, 'message': message})
            else: # tardy
                time_status = 0
                status = "Tardy"
                message = "you are tardy, please submit your attendance and leave an excuse for your tardiness."
                return render(request, 'student_view/check_in.html', {'student_status':status, 'message': message})
    if request.method == 'POST':
        # TO DO -- write into databases
        if not request.POST.get('excuse'):
            return render(request, 'student_view/check_in.html', {'student_status':status, 'error':True})
        query = Attendance(userId= request.user, tardy = True if status == "tardy" else False, absent = True if status == "absent" else False, excuse=request.POST.get('excuse'))
        query.save()
    # redirect to 'congrats, you've submitted' page
    return render(request, 'student_view/check_in.html', {'student_status':status})

@login_required
def student_info(request):
    student = Students.objects.all().filter(userId_id=request.session['id'])
    user = User.objects.all().filter(id=request.session['id'])
    return render(request, 'student_view/student_user_info.html', {'first_name': user[0].first_name, 'last_name': user[0].last_name, 'program': student[0].program, 'cohort': student[0].cohort, 'location':student[0].location, 'email':user[0].email})

#the below is not yet complete
#viewing student records for everyone
@login_required
def view_records(request):
    if request.method == GET:
        #determine which user is trying to view records
        user = request.user.username
        return render(request, 'registration/login.html', None)


@login_required
def view_profile(request):
    pass
    #this is for all users 
    #all users should be able to post as well as get 



# VIEWS FOR STUDENT_VIEW
class HomePageView(TemplateView):
    template_name = 'student_view/index.html'
class CheckInView(TemplateView):
    template_name = 'student_view/check_in.html'
class CheckInLateView(TemplateView):
    template_name = 'student_view/check_in_late.html'
class NotOnCampusView(TemplateView):
    template_name = 'student_view/not_on_campus.html'
class ViewRecordView(TemplateView):
    template_name = 'student_view/view_record.html'
class StudentInfoView(TemplateView):
    template_name = 'student_view/student_user_info.html'



#VIEWS FOR GLOBAL ADMIN
class LocationView (TemplateView):
    template_name = "global_admin_view/location_view.html"
class AdminProfileView (TemplateView):
    template_name = "global_admin_view/admin_profile.html"


class KenyaAndEastView (TemplateView):
    template_name = "global_admin_view/school_views/kenya_and_east_africa/kenya_and_east_africa.html"
class KenyaAndEastLocalAdminsView (TemplateView):
    template_name = "global_admin_view/school_views/kenya_and_east_africa/kenya_local_admins.html"
class KenyaAndEastStudentsView (TemplateView):
    template_name = "global_admin_view/school_views/kenya_and_east_africa/kenya_students.html"
class KenyaAndEastSchoolView (TemplateView):
    template_name = "global_admin_view/school_views/kenya_and_east_africa/kenya_school.html"


class NigeriaView (TemplateView):
    template_name = "global_admin_view/school_views/nigeria/nigeria.html"
class NigeriaLocalAdminsView (TemplateView):
    template_name = "global_admin_view/school_views/nigeria/nigeria_local_admins.html"
class NigeriaStudentsView (TemplateView):
    template_name = "global_admin_view/school_views/nigeria/nigeria_students.html"
class NigeriaSchoolView (TemplateView):
    template_name = "global_admin_view/school_views/nigeria/nigeria_school.html"


class GhanaView (TemplateView):
    template_name = "global_admin_view/school_views/ghana/ghana.html"
class GhanaLocalAdminsView (TemplateView):
    template_name = "global_admin_view/school_views/ghana/ghana_local_admins.html"
class GhanaStudentsView (TemplateView):
    template_name = "global_admin_view/school_views/ghana/ghana_students.html"
class GhanaSchoolView (TemplateView):
    template_name = "global_admin_view/school_views/ghana/ghana_school.html"



class InternationalOtherView (TemplateView):
    template_name = "global_admin_view/school_views/international_and_other/international_and_other.html"
class InternationalOtherLocalAdminsView (TemplateView):
    template_name = "global_admin_view/school_views/international_and_other/international_and_other_local_admins.html"
class InternationalOtherStudentsView (TemplateView):
    template_name = "global_admin_view/school_views/international_and_other/international_and_other_students.html"
class InternationalOtherSchoolView (TemplateView):
    template_name = "global_admin_view/school_views/international_and_other/international_and_other_school.html"



