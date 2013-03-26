from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from django.views.generic import TemplateView

from settings import THISAPP

USERNAME_RE = r'(?P<owner_username>[^/?]+)'
ID2_RE = r'(?P<id2>[^/?]+)'

username_url_re_prefix = r'^' + USERNAME_RE 
username_id2_url_re_prefix = username_url_re_prefix + r'/' + ID2_RE
suffix = r'/$'

#all urls names are of the type: THISAPP+'_'+view_name
urls = [
    ('index_all',r'^$'),
    ('index_user', username_url_re_prefix + suffix),
    ('create_list', username_url_re_prefix + r'/create' + suffix),
    ('update_list', username_id2_url_re_prefix + r'/update' + suffix),
    ('bulk_action', username_url_re_prefix + r'/bulk_action' + suffix),
    ('detail', username_id2_url_re_prefix + suffix),
]

#dictionnary: short names (without app preffix) to long names (with app preffix)
URLS_THISAPP = { u[0]:THISAPP+'_'+u[0] for u in urls }

urlpatterns = patterns(THISAPP+'.views',
   *[  url(u[1],u[0],name=URLS_THISAPP[u[0]]) for u in urls ]
)
