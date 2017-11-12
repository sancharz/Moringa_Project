from django.conf.urls import url
from moringa_main_app import views

urlpatterns = [
    #URLS for LOGIN
    # url(r'^login$', auth_views.login, {'template_name': 'login.html'} name='login'),

    #URLS for Student View
    url(r'^$', views.HomePageView.as_view()),
    url(r'^check_in/$', views.CheckInView.as_view()),
    url(r'^check_in_late/$', views.CheckInLateView.as_view()),
    url(r'^not_on_campus/$', views.NotOnCampusView.as_view()),
    url(r'^view_record/$', views.ViewRecordView.as_view()),
    url(r'^student_profile/$', views.StudentProfileView.as_view()),


    # URLS for Global Admin View
    url(r'^global_home$', views.LocationView.as_view()),
    url(r'^global_admin_profile$', views.GlobalAdminProfileView.as_view()),
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

    # URLS for Local Admin View
    url(r'^local_home$', views.LocalAdminHomeView.as_view()),
    url(r'^local_admin_profile$', views.LocalAdminProfileView.as_view()),
    url(r'^attendance_history$', views.AttendanceHistoryView.as_view()),
    url(r'^student_information$', views.StudentInformationView.as_view()),

]
