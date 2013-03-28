from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url

import settings

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^master-checkbox/', include('master_checkbox.urls')),

    url(r'^users/', include('userena.urls')),

    url(r'^django_tables2_datatables/', include('django_tables2_datatables.urls')),
    url(r'^user-lists/', include('user_user_groups.urls')),
    url(r'^uri-lists/', include('user_list_uri.urls')),
    url(r'^issue-tracker/', include('issue_tracker.urls')),
)

#to serve static files:

urlpatterns += staticfiles_urlpatterns()
