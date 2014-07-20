from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from leave.views import LeaveAPI, LeaveTypeAPI, LeaveTypeFormView, HolidayFormView, HolidayAPI, SubscriberLeaveAPI, LeaveApproveView, ApproverLeaveAPI
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ola.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', csrf_exempt(LeaveAPI.as_view()), name='leave'),
    url(r'^/type$', csrf_exempt(LeaveTypeAPI.as_view()), name='leave_type'),
    url(r'^/type/view$', LeaveTypeFormView.as_view(), name='leave_type_form'),
    url(r'^/holiday$', csrf_exempt(HolidayAPI.as_view()), name='holiday'),
    url(r'^/holiday/view$', HolidayFormView.as_view(), name='holiday_view'),
    url(r'^/subscriber/([\d]+)$', csrf_exempt(SubscriberLeaveAPI.as_view()), name='subscriber_leave_details'),
    url(r'^/pending/approval/view$', LeaveApproveView.as_view(), name='leave_approve_view'),
    url(r'^/approver/([\d]+)$', csrf_exempt(ApproverLeaveAPI.as_view()), name='approver_pending_leaves'),
)
