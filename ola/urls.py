from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ola.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/login', 'django.contrib.auth.views.login'),
    (r'^logout', 'django.contrib.auth.views.logout_then_login'),
    url(r'^accounts/registration$', 'subscriber.views.register'),
    url(r'^api/subscriber', include('subscriber.urls')),
    url(r'^', include('leave.urls')),
)
