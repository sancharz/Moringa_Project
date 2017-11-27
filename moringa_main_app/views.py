from django.shortcuts import render, redirect
from django.views.generic import TemplateView
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
# check in for students - Anna Lou
@login_required
def check_in(request):
    message = "" # initialize a variable to hold a message based on student status
    status = "" # initialize a variable to hold a student status
    tardy = True
    absent = True

    # check if student has already submitted attendance today
    #rows = Attendance.objects.filter(date__date=datetime.now().date()) 
    rows = Attendance.objects.filter(date__date=datetime.now().date(), user_id=request.user.id) 
    if len(rows) > 0:
        return redirect('/view_record/')
    tardy = False
    absent = False

    # get user's IP address --> https://github.com/un33k/django-ipware
    ip = get_ip(request)
    if not ip: # if IP address not retrieved (error check)
        print("we don't have an IP address for user")
    
    if ip == MORINGA_IP_ADDRESS: # on campus
        # check time
        if datetime.now().time() <= datetime.strptime('080000', '%H%M%S').time(): # on time
            tardy = False
            absent = False
            status = "On Time"
            message = "You are on time. Please submit your attendance."
            
        else: # tardy
            status = "Tardy"
            absent = False
            message = "You are tardy. Please leave an excuse for your tardiness."
    
    else: # not on campus
        status = "Not on Campus"
        tardy = False
        message = "You are not currently on campus. If applicable, please leave an excuse for your absence."
        
    if request.method == 'GET': # render page
        return render(request, 'student_view/check_in.html', {'student_status':status, 'message':message})

    if request.method == 'POST': # add to database
        excuse = ""
        if status != "On Time": # should be an excuse
            if not request.POST.get('excuse'): # missing excuse
                return render(request, 'student_view/check_in.html', {'student_status':status, 'message': message, 'error':True})
            else: # excuse exists
                excuse = request.POST.get('excuse')

        query = Attendance(tardy=tardy, absent=absent, excuse=excuse, user_id=request.user.id) 
        query.save() # save into attendance database

    # redirect to view records
    return redirect('/view_record/')

#viewing a student profile is read only so there is no POST - Sela and Emily Lu
#student cannot edit their profile information
@login_required
def student_info(request):
    student = Students.objects.filter(user = request.user) #made changes -sancharz
    cur_user = User.objects.filter(username = request.user)
    #return render(request, 'student_view/student_user_info.html', {'first_name': user[0].first_name, 'last_name': user[0].last_name, 'program': student[0].program, 'cohort': student[0].cohort, 'location':student[0].location, 'email':user[0].email})
    return render(request, 'student_view/student_user_info.html', {'first_name': cur_user[0].first_name, 'last_name': cur_user[0].last_name, 'program': student[0].program, 'cohort': student[0].cohort, 'location':student[0].location, 'email':cur_user[0].email})


#viewing student records for everyone
@login_required
def view_record(request):
    #determine which user is trying to view records
    user = request.user.username
    #rows = Attendance.objects.all()
    rows = Attendance.objects.filter(user_id=request.user.id)
    status = []
    for row in rows:
        if row.tardy:
            status.append('Tardy')
        elif row.absent:
            status.append('Absent')
        else:
            status.append('On Time')
    return render(request, 'student_view/view_record.html', {'list': zip(rows, status)})

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
    if local_a:
        return render(request, 'global_admin_view/admin_profile.html', {
            'first_name': cur_user[0].first_name,
            'last_name': cur_user[0].last_name,
            'program': local_a[0].program,
            'location': local_a[0].location,
            'email': cur_user[0].username,
            'admin_type': "local"
        })
    if global_a:
        #note that global admin does not have program, cohort or location
        return render(request, 'global_admin_view/admin_profile.html', {
            'first_name': cur_user[0].first_name,
            'last_name': cur_user[0].last_name,
            'email': cur_user[0].username,
            'admin_type': "global"

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
                'location': local_a[0].location,
                'email': cur_user[0].username,
                'admin_type': "local"
            })
        if request.method == 'POST':
            cur_user.update(first_name = request.POST.get("firstname"))
            cur_user.update(last_name = request.POST.get("lastname"))
            local_a.update(program = request.POST.get("program"))
            local_a.update(location = request.POST.get("location"))
            cur_user.update(email = request.POST.get("email"))

            return redirect('/view_profile')


    if global_a:
        if request.method == 'GET':
            # note that global admin does not have program, cohort or location
            return render(request, 'global_admin_view/edit_profile.html', {
                'first_name': cur_user[0].first_name,
                'last_name': cur_user[0].last_name,
                'email': cur_user[0].username,
                'admin_type': "global"
            })
        if request.method == 'POST':
            cur_user.update(first_name = request.POST.get("firstname"))
            cur_user.update(last_name = request.POST.get("lastname"))
            global_a.update(program = request.POST.get("program"))
            global_a.update(location = request.POST.get("location"))
            cur_user.update(email = request.POST.get("email"))

            return redirect('/view_profile')


    



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
class GlobalHome (TemplateView):
    template_name = "global_admin_view/global_home.html"

class LocationView (TemplateView):
    template_name = "global_admin_view/location_view.html"

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



