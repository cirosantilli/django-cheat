from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from django.views.generic import TemplateView

import polls.views
from polls.models import Poll

#urlpatterns takes a list of tuples

urlpatterns = patterns('polls.views',

    ##without generic templates:
    #url(r'^$', 'index'),
    #url(r'^(?P<poll_id>\d+)/$', 'detail'),
    #url(r'^(?P<poll_id>\d+)/results/$', 'results'),
    #url(r'^(?P<poll_id>\d+)/vote/$', 'vote

    #url(r'^$',
            #'index',
            #name='poll_index'),

    #with generic templates:
    url(r'^$',
            ListView.as_view( #premade view: list of object
                        queryset=Poll.objects.order_by('-pub_date'), #I think this is lazy, so with paginator no problem!
                        context_object_name='items', #object passed to the template
                        template_name='polls/index.html', #template is uses. has default <app_name>/<model_name>_list.html
                        paginate_by = polls.views.ITEMS_PER_PAGE, #you can paginate here!
                    ),
            name='poll_index'), #to refer to its url with reverse (and so url in templates). therefore, this must be unique
    #but I find this more confusing...

    url(r'^create/$', 
        'create',
        name='poll_create'),

    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Poll, #which model is being detailed
            context_object_name='item', #object passed to the template
            template_name='polls/detail.html'), #has default teplate <app_name>/<model_name>_detail.html
        name='poll_detail'),

    url(r'^(?P<pk>\d+)/results/$',
        DetailView.as_view(
            model=Poll,
            template_name='polls/results.html'),
        name='poll_results'),

    url(r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)
