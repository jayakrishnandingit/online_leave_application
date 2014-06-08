from django.conf.urls import patterns, include, url
from views import HomeView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ola.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/login', 'django.contrib.auth.views.login'),
    (r'^logout', 'django.contrib.auth.views.logout_then_login'),
    url(r'^$', HomeView.as_view(), name='home_page'),
    url(r'^subscriber', include('subscriber.urls')),
    url(r'^leave', include('leave.urls')),
)
