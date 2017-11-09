from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
import datetime

# developer admin page
def index(request):
    context = "some context here"
    return render(request, 'templates/student_view/index.html', context)

# login
def login(request):
    context = "some context here"
    return render(request, 'templates/student_view/index.html', context)

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



