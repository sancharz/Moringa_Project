from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'index.html'

class CheckInView(TemplateView):
    template_name = 'check_in.html'

class CheckInLateView(TemplateView):
    template_name = 'check_in_late.html'

class NotOnCampusView(TemplateView):
    template_name = 'not_on_campus.html'

class ViewRecordView(TemplateView):
    template_name = 'view_record.html'