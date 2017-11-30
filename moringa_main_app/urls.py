from django.conf.urls import url
from django.conf import settings
from moringa_main_app import views
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views

urlpatterns = [
    #index page URL Mapping - there are two for now but one will have to be deleted
    url(r'^$', views.index, name='index'),
    #url(r'^index/$', views.index, name='index'),

    #LOGIN AND SIGN-UP URL mappings 
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    #STUDENT URL Mappings 
    url(r'^check_in/$', views.check_in, name='check_in'),
    url(r'^view_record/$', views.view_record, name='view_record'),
    url(r'^student_info/$', views.student_info, name='student_user_info'),

    #LOCAL ADMIN URL Mappings 
    url(r'^view_profile/$', views.view_profile, name='admin_profile'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^local_home/$', views.LocalHome.as_view()),

    #GLOBAL ADMIN URL Mappings 
    url(r'^global_home/$', views.GlobalHome.as_view()),
    url(r'^location_view$', views.location_view, name="location_view"),
    url(r'^admin_profile$', views.AdminProfileView.as_view()),
    


#hard coded Url mappings no longer necessary - sancharz
    # url(r'^check_in_late/$', views.CheckInLateView.as_view()),
    # url(r'^not_on_campus/$', views.NotOnCampusView.as_view()),
#see comment above for explanation of comment out

#looks like the following hardcoded URL mappings will no longer be necessary - sancharz
    # url(r'^kenya_and_east_africa$', views.KenyaAndEastView.as_view()),
    # url(r'^kenya_and_east_africa_local_admins$', views.KenyaAndEastLocalAdminsView.as_view()),
    # url(r'^kenya_and_east_africa_students$', views.KenyaAndEastStudentsView.as_view()),
    # url(r'^kenya_and_east_africa_school$', views.KenyaAndEastSchoolView.as_view()),
    # url(r'^nigeria$', views.NigeriaView.as_view()),
    # url(r'^nigeria_local_admins$', views.NigeriaLocalAdminsView.as_view()),
    # url(r'^nigeria_students$', views.NigeriaStudentsView.as_view()),
    # url(r'^nigeria_school$', views.NigeriaSchoolView.as_view()),
    # url(r'^ghana$', views.GhanaView.as_view()),
    # url(r'^ghana_local_admins$', views.GhanaLocalAdminsView.as_view()),
    # url(r'^ghana_students$', views.GhanaStudentsView.as_view()),
    # url(r'^ghana_school$', views.GhanaSchoolView.as_view()),
    # url(r'^international_and_other$', views.InternationalOtherView.as_view()),
    # url(r'^international_and_other_local_admins$', views.InternationalOtherLocalAdminsView.as_view()),
    # url(r'^international_and_other_students$', views.InternationalOtherStudentsView.as_view()),
    # url(r'^international_and_other_school$', views.InternationalOtherSchoolView.as_view()),
#see comment above for explanation of the above comment out - sancharz
    
]
