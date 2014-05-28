from django.conf.urls import patterns, include, url
from views import SubscriberView, SubscriberDetailsView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('subscriber',
    # Examples:
    # url(r'^$', 'ola.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', csrf_exempt(SubscriberView.as_view())),
    url(r'^/([\w]+)$', SubscriberDetailsView.as_view()),
)
