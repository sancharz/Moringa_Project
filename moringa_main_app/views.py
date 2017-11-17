from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from moringa_main_app.models import Attendance
import datetime

# developer admin page
def index(request):
    return render(request, 'student_view/index.html', None)

# register
def register(request):
    if request.method == 'GET':
        return render(request, 'REGISTER.HTML FIX THIS', None)
    else:
        # INSERT DATA IN STUDENT/LOCAL_ADMIN/GLOBAL_ADMIN & USER TABLES THROUGH FIELDS IN HTML PAGE
        # REDIRECT TO APPROPRIATE HOME PAGE
    
# login
def login(request):
    if request.method == 'GET':
        return render(request, 'LOGIN.HTML FIX THIS', None)
    else:
        # make time_status && location_status 
        # time_status == 1 (on time); == 0 (late)
        # location_status == 1 (on campus); == 0 (not on campus)
        # check location
        message = "" # initialize a variable to hold a message based on student status
        status = "" # initialize a variable to hold a student status
        location_status = 0 # default not on campus
        if STUDENTONCAMPUS: # condition for if on campus
            location_status = 1
        
        if location_status == 0: # if not on campus, render absent page
            status = "Not on Campus"
            message = "You are not currently on campus. If applicable, please leave an excuse for your absence."
            return render(request, 'student_view/check_in.html', {'student_status':status, 'message': message})
        else: # only check time if student is on campus
            time_status = 0 # default late
            if STUDENTONTIME: # condition for if on time
                time_status = 1
                status = "On Time"
                message = "you are on time. please submit your attendance!"
                return render(request, 'student_view/check_in.html', {'student_status':status, 'message': message})
            else: # student is tardy, render tardy page
                status = "Tardy"
                message = "you are tardy, please submit your attendance and leave an excuse for your tardiness."
                return render(request, 'student_view/check_in.html', {'student_status':status, 'message': message})

# check in
def check_in(request):
    status = "on time"
    if True: #condition for checking time
        status = "tardy"
    if request.method == 'POST':
        if not request.POST.get('excuse'):
            return render(request, 'student_view/check_in.html', {'student_status':status, 'error':True})
        query = Attendance(userId=request.user, tardy=True if status == "tardy" else False, absent=True if status == "absent" else False, excuse=request.POST.get('excuse'))
        query.save()
        # redirect to 'congrats, you've submitted' page
    return render(request, 'student_view/check_in.html', {'student_status':status})

# display student info
def student_info(request):
    # select currently logged in user
    student = Students.objects.all().filter(userId_id=request.session['id']) # need data from student table
    user = User.objects.all().filter(id=request.session['id']) # need data from user table
    return render(request, 'student_view/student_user_info.html', {'first_name': user[0].first_name, 'last_name': user[0].last_name, 'program': student[0].program, 'cohort': student[0].cohort, 'location':student[0].location, 'email':user[0].email})

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



