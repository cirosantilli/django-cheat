from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView

from settings import THISAPP

PK_RE = r'(?P<pk>\d+)'
suffix = r'/$'

#all urls names are of the type: THISAPP+'_'+view_name
urls = [
    ('index_all',r'^$'),
    ('detail', '^detail/' + PK_RE + suffix),
    ('create_issue', r'^create' + suffix),
]

#dictionnary: short names (without app preffix) to long names (with app preffix)
URLS_THISAPP = { u[0]:THISAPP+'_'+u[0] for u in urls }

urlpatterns = patterns(THISAPP+'.views',
   *[  url(u[1],u[0],name=URLS_THISAPP[u[0]]) for u in urls ]
)
