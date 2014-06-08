from django.conf.urls import patterns, include, url
from leave.views import LeaveTypeAPI, LeaveTypeFormView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ola.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^/type$', LeaveTypeAPI.as_view(), name='leave_type'),
    url(r'^/type/view$', LeaveTypeFormView.as_view(), name='leave_type_form'),
)
