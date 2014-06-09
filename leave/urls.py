from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from leave.views import LeaveTypeAPI, LeaveTypeFormView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ola.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^/type$', csrf_exempt(LeaveTypeAPI.as_view()), name='leave_type'),
    url(r'^/type/view$', LeaveTypeFormView.as_view(), name='leave_type_form'),
)
