from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

import settings

urlpatterns = patterns(
    '',
    url
    (
        '^static/js/main.js$',
        TemplateView.as_view(
            template_name = settings.THISAPP+'/media/js/master-checkbox.js',
            get_context_data = lambda: settings.CONTEXT,
            #extra_context = settings.CONTEXT,
        ),
        name = settings.THISAPP+"_js",
    ),
)
