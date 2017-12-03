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
    url(r'^login/signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    #STUDENT URL Mappings 
    url(r'^check_in/$', views.check_in, name='check_in'),
    url(r'^view_record/$', views.view_record, name='view_record'),
    url(r'^student_info/$', views.student_info, name='student_user_info'),

    #LOCAL ADMIN URL Mappings 
    url(r'^view_profile/$', views.view_profile, name='admin_profile'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^local_admin/$', views.local_admin, name='local_admin'),

    #GLOBAL ADMIN URL Mappings 
    url(r'^global_admin/$', views.global_admin, name='global_admin'),
    url(r'^global_home/$', views.global_admin, name='global_home'),
    url(r'^edit_information_global/$', views.edit_information_global, name='edit_information_global'),
    url(r'^edit_information_local/$', views.edit_information_local, name='edit_information_local'),
    #do we want the admin_profile to be as_view?? - Sancharz to Jun?
    url(r'^admin_profile$', views.AdminProfileView.as_view()),
    
]
