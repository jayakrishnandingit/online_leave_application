from django.conf.urls import patterns, include, url
from views import SubscriberAPI, ApproverAPI, SubscriberView, SubscriberDetailsFormView, SubscriberDetailsAPI, SubscriberCreateView, SubscriberRegistrationView, SubscriberNotificationAPI
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('subscriber',
	# Examples:
	# url(r'^$', 'ola.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),
	url(r'^$', csrf_exempt(SubscriberAPI.as_view())),
	url(r'^/approvers$', csrf_exempt(ApproverAPI.as_view())),
	url(r'^/registration$', csrf_exempt(SubscriberRegistrationView.as_view()), name='admin_registration'),
	url(r'^/create$', SubscriberCreateView.as_view(), name='create_subscriber'),
	url(r'^/view$', SubscriberView.as_view(), name='view_subscribers'),
	url(r'^/([\w]+)/details$', SubscriberDetailsFormView.as_view(), name='subscriber_details'),
	url(r'^/([\w]+)$', csrf_exempt(SubscriberDetailsAPI.as_view())),
	url(r'^/([\d]+)/notifications$', csrf_exempt(SubscriberNotificationAPI.as_view()), name='subscriber_notifications'),
)
