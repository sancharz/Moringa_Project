from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Imported exemption decorator to test code
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
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
    return render(request, 'registration/login.html')

# login
def login(request):

    if request.method == "GET":
        return render(request, 'login_view/login.html')
    # return render(request, 'student_view/index.html', None)

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
                return redirect('/local_home/')
            if query_ga:
                #user is a ga
                return redirect('/global_home/')


            #commented this code out to test if alternative above works - sancharz to Romil
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

#viewing a student profile is read only so there is no POST
#student cannot edit their profile information
@login_required
def student_info(request):
    student = Students.objects.filter(user = request.user) #made changes -sancharz
    cur_user = User.objects.filter(username = request.user)
    #return render(request, 'student_view/student_user_info.html', {'first_name': user[0].first_name, 'last_name': user[0].last_name, 'program': student[0].program, 'cohort': student[0].cohort, 'location':student[0].location, 'email':user[0].email})
    return render(request, 'student_view/student_user_info.html', {'first_name': cur_user[0].first_name, 'last_name': cur_user[0].last_name, 'program': student[0].program, 'cohort': student[0].cohort, 'location':student[0].location, 'email':cur_user[0].email})


#the function below is not yet complete - NOT DONE
#SELA AND  EMILY LU
#viewing student records for everyone
@login_required
def view_records(request):
    if request.method == GET:
        #determine which user is trying to view records
        user = request.user.username
        return render(request, 'registration/login.html', None)

#this function is not yet done - NOT DONE
#SELA and EMILY LU
#Task - should be able to view and edit their information
#this is only for local admin and global admin (similar to student_info() above)
@login_required
def view_profile(request):
    #task - also have get or post 
    #query the database
    local_a = LocalAdmin.objects.filter(user = request.user)
    global_a = GlobalAdmin.objects.filter(user = request.user)
    cur_user = User.objects.filter(username = request.user)
    #only two of these query sets will not be empty
    #user can't be local_a and global_a at the same time
    #TODO: I added user_type so i can check what type of user they are in admin_profile.html, is there better way?
    if local_a:
        if request.method == 'GET':
            return render(request, 'global_admin_view/admin_profile.html', {
                'first_name': cur_user[0].first_name,
                'last_name': cur_user[0].last_name,
                'program': local_a[0].program,
                'cohort': "",
                'location': local_a[0].location,
                'email':cur_user[0].email,
                'user_type': "local_admin"
            })

    if global_a:
        if request.method == 'GET':
            #note that global admin does not have program, cohort or location
            return render(request, 'global_admin_view/admin_profile.html', {
                'first_name': cur_user[0].first_name,
                'last_name': cur_user[0].last_name,
                'program': "haibo",
                'cohort': "",
                'location': "",
                'email': cur_user[0].email,
                'user_type': "global_admin"
            })

@login_required
def edit_profile(request):
    # task - also have get or post
    # query the database
    local_a = LocalAdmin.objects.filter(user=request.user)
    global_a = GlobalAdmin.objects.filter(user=request.user)
    cur_user = User.objects.filter(username=request.user)
    # only two of these query sets will not be empty
    # user can't be local_a and global_a at the same time
    if local_a:
        if request.method == 'GET':
            return render(request, 'global_admin_view/edit_profile.html', {
                'first_name': cur_user[0].first_name,
                'last_name': cur_user[0].last_name,
                'program': local_a[0].program,
                'cohort': "",
                'location': local_a[0].location,
                'email': cur_user[0].email,
                'user_type': "local_admin"
            })
        if request.method == 'POST':
            #TODO: Update the User's info using the input, redirect?
            cur_user[0].first_name = request.POST.get("firstname")
            cur_user[0].last_name = request.POST.get("lastname")
            local_a[0].program = request.POST.get("program")
            #TODO: cohort is nothing?
            local_a[0].location = request.POST.get("location")
            cur_user[0].email = request.POST.get("email")

            cur_user.save()
            local_a.save()


    if global_a:
        if request.method == 'GET':
            # note that global admin does not have program, cohort or location
            return render(request, 'global_admin_view/edit_profile.html', {
                'first_name': cur_user[0].first_name,
                'last_name': cur_user[0].last_name,
                'program': "haibo",
                'cohort': "",
                'location': "",
                'email': cur_user[0].email,
                'user_type': "global_admin"
            })
        if request.method == 'POST':
            # TODO: Update the User's info using the input, redirect?
            cur_user[0].first_name = request.POST.get("firstname")
            cur_user[0].last_name = request.POST.get("lastname")
            global_a[0].program = request.POST.get("program")
            # TODO: cohort is nothing?
            global_a[0].location = request.POST.get("location")
            cur_user[0].email = request.POST.get("email")

            cur_user.save()
            global_a.save()



# VIEW FOR LOGIN
# class LogInView(TemplateView):
#     template_name = 'login_view/login.html'

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
class StudentProfileView(TemplateView):
    template_name = 'student_view/student_profile.html'


#VIEWS FOR GLOBAL ADMIN
@csrf_exempt
def location_select (request):
    if request.method == 'GET':
        return render(request, 'global_admin_view/global_home.html')
    if request.method == 'POST':
        # Get the user's selected location
        location = request.POST.get("location")
        # TODO: Query database, join students/attendance using "user" and query for all with location as requirement
        students = Students.objects.filter(location=location)
        # Render home template, passing in students queryset as context
        return render(request, 'global_admin_view/global_home.html', {"students":students})



class LocationView (TemplateView):
    template_name = "global_admin_view/global_home.html"

class GlobalAdminProfileView (TemplateView):
    template_name = "global_admin_view/global_admin_profile.html"

class AdminProfileView (TemplateView):
    template_name = "global_admin_view/admin_profile.html"


#Views for Local Admin
class LocalHome (TemplateView):
    template_name = "local_admin/localadmin_home.html"


#commented out the brute-force coded classes as we will not be using them - sancharz

# class KenyaAndEastView (TemplateView):
#     template_name = "global_admin_view/school_views/kenya_and_east_africa/kenya_and_east_africa.html"
# class KenyaAndEastLocalAdminsView (TemplateView):
#     template_name = "global_admin_view/school_views/kenya_and_east_africa/kenya_local_admins.html"
# class KenyaAndEastStudentsView (TemplateView):
#     template_name = "global_admin_view/school_views/kenya_and_east_africa/kenya_students.html"
# class KenyaAndEastSchoolView (TemplateView):
#     template_name = "global_admin_view/school_views/kenya_and_east_africa/kenya_school.html"


# class NigeriaView (TemplateView):
#     template_name = "global_admin_view/school_views/nigeria/nigeria.html"
# class NigeriaLocalAdminsView (TemplateView):
#     template_name = "global_admin_view/school_views/nigeria/nigeria_local_admins.html"
# class NigeriaStudentsView (TemplateView):
#     template_name = "global_admin_view/school_views/nigeria/nigeria_students.html"
# class NigeriaSchoolView (TemplateView):
#     template_name = "global_admin_view/school_views/nigeria/nigeria_school.html"


# class GhanaView (TemplateView):
#     template_name = "global_admin_view/school_views/ghana/ghana.html"
# class GhanaLocalAdminsView (TemplateView):
#     template_name = "global_admin_view/school_views/ghana/ghana_local_admins.html"
# class GhanaStudentsView (TemplateView):
#     template_name = "global_admin_view/school_views/ghana/ghana_students.html"
# class GhanaSchoolView (TemplateView):
#     template_name = "global_admin_view/school_views/ghana/ghana_school.html"



# class InternationalOtherView (TemplateView):
#     template_name = "global_admin_view/school_views/international_and_other/international_and_other.html"
# class InternationalOtherLocalAdminsView (TemplateView):
#     template_name = "global_admin_view/school_views/international_and_other/international_and_other_local_admins.html"
# class InternationalOtherStudentsView (TemplateView):
#     template_name = "global_admin_view/school_views/international_and_other/international_and_other_students.html"
# class InternationalOtherSchoolView (TemplateView):
#     template_name = "global_admin_view/school_views/international_and_other/international_and_other_school.html"



#VIEWS FOR LOCAL ADMIN
class LocalAdminHomeView (TemplateView):
    template_name = "local_admin_view/local_admin_home.html"
class LocalAdminProfileView (TemplateView):
    template_name = "local_admin_view/local_admin_profile.html"
class AttendanceHistoryView (TemplateView):
    template_name = "local_admin_view/attendance_history.html"
class StudentInformationView (TemplateView):
    template_name = "local_admin_view/student_information.html"





