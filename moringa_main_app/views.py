from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from moringa_main_app.forms import SignUpForm
from django.http import HttpResponseRedirect, HttpResponse


#LOGIN - Emily Hong and Jun
    #Get request - displaying the login page
    #POst - read in email and password 
    #authenticate (if not correct - login failed)
    #if password correct - determine what type of user from all users
    #redirect to appropriate page - student/local/admin
    #if user is student - take note of time/IP address and render appropraiate page based on time

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

# check in
def check_in(request):
    status = "on time"
    if request.session['student_status'] == 'tardy': #condition for checking time
        status = "tardy"
    if request.method == 'POST':
        if not request.POST.get('excuse'):
            return render(request, 'student_view/check_in.html', {'student_status':status, 'error':True})
        query = Attendance(userId=request.user, tardy=True, absent=False, excuse=request.POST.get('excuse'))
        query.save()
        # redirect to 'congrats, you've submitted' page
    return render(request, 'student_view/check_in.html', {'student_status':status})

def student_info(request):
    student = Students.objects.all().filter(userId_id=request.session['id'])
    user = User.objects.all().filter(id=request.session['id'])
    return render(request, 'student_view/student_user_info.html', {'first_name': user[0].first_name, 'last_name': user[0].last_name, 'program': student[0].program, 'cohort': student[0].cohort, 'location':student[0].location, 'email':user[0].email})


#SUBMIT Button - Late
    #writes to the attendace table based on the attendance 

#Local_admin
    #query the database (SQL statements requoired)
    #dynamically display info

#Global_admin
    # pick location and redirect to location info

#global_admin view info
    #query the database (SQL statements requoired)
    #dynamically display info



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



