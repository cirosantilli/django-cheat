import os

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

import settings

thisapp = os.path.split(os.path.dirname(os.path.abspath(__file__)))[1]

urlpatterns = patterns('',

    url('^media/js/jquery.dataTables.config.js$',
        TemplateView.as_view(
            template_name = thisapp+'/media/js/jquery.dataTables.config.js',
            #extra_context = settings.CONTEXT,
            get_context_data = lambda: settings.CONTEXT,
        ),
        name="django_tables2_datatables_config_js",
    ),

)

