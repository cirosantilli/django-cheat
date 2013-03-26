from django.conf.urls import patterns, include, url

from django.views.generic import TemplateView

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',

    url('^$',
        direct_to_template, #function to call
        {'template': 'home.html'}, #args for direct_to_template
        name="home" #hame for url template
    ),
    #home page 

    url('^about/$',
        TemplateView.as_view,
        {'template_name': 'about.html'},
        "about"
    ),
    #static page, simple generic view

    url(r'^polls/', include('polls.urls')),
    #mounts all the admin urls defined in admin.site.urls on top of admin/

    url(r'^admin/', include(admin.site.urls)),

    #<userena
    url(r'^accounts/', include('userena.urls')),
    #</userena
)

urlpatterns += staticfiles_urlpatterns() #to serve static files