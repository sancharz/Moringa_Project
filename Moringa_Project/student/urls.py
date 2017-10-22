from django.conf.urls import url
from student import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^check_in/$', views.CheckInView.as_view()),
    url(r'^check_in_late/$', views.CheckInLateView.as_view()),
    url(r'^not_on_campus/$', views.NotOnCampusView.as_view()),
    url(r'^view_record/$', views.ViewRecordView.as_view()),

]