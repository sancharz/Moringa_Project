from django.conf.urls import url
from django.conf import settings
from moringa_main_app import views
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views

urlpatterns = [
    #URLS for Student View
    url(r'^$', views.HomePageView.as_view()),
    url(r'^check_in/$', views.CheckInView.as_view()),
    url(r'^check_in_late/$', views.CheckInLateView.as_view()),
    url(r'^not_on_campus/$', views.NotOnCampusView.as_view()),
    url(r'^view_record/$', views.ViewRecordView.as_view()),
    url(r'^student_info/$', views.StudentInfoView.as_view()),


    # URLS for Global Admin View
    url(r'^location_view$', views.LocationView.as_view()),
    url(r'^admin_profile$', views.AdminProfileView.as_view()),
    url(r'^kenya_and_east_africa$', views.KenyaAndEastView.as_view()),
    url(r'^kenya_and_east_africa_local_admins$', views.KenyaAndEastLocalAdminsView.as_view()),
    url(r'^kenya_and_east_africa_students$', views.KenyaAndEastStudentsView.as_view()),
    url(r'^kenya_and_east_africa_school$', views.KenyaAndEastSchoolView.as_view()),
    url(r'^nigeria$', views.NigeriaView.as_view()),
    url(r'^nigeria_local_admins$', views.NigeriaLocalAdminsView.as_view()),
    url(r'^nigeria_students$', views.NigeriaStudentsView.as_view()),
    url(r'^nigeria_school$', views.NigeriaSchoolView.as_view()),
    url(r'^ghana$', views.GhanaView.as_view()),
    url(r'^ghana_local_admins$', views.GhanaLocalAdminsView.as_view()),
    url(r'^ghana_students$', views.GhanaStudentsView.as_view()),
    url(r'^ghana_school$', views.GhanaSchoolView.as_view()),
    url(r'^international_and_other$', views.InternationalOtherView.as_view()),
    url(r'^international_and_other_local_admins$', views.InternationalOtherLocalAdminsView.as_view()),
    url(r'^international_and_other_students$', views.InternationalOtherStudentsView.as_view()),
    url(r'^international_and_other_school$', views.InternationalOtherSchoolView.as_view()),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    
]
