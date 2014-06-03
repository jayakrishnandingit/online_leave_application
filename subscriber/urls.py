from django.conf.urls import patterns, include, url
from views import SubscriberAPI, SubscriberView, SubscriberDetailsView, SubscriberCreateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('subscriber',
	# Examples:
	# url(r'^$', 'ola.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),
	url(r'^$', csrf_exempt(SubscriberAPI.as_view())),
	url(r'^/create$', SubscriberCreateView.as_view(), name='create_subscriber'),
	url(r'^/view$', SubscriberView.as_view(), name='view_subscribers'),
	url(r'^/([\w]+)$', SubscriberDetailsView.as_view(), name='subscriber_details'),
)
