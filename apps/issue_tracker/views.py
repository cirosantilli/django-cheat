from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory, model_to_dict
from django.forms.widgets import SelectMultiple
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods, require_safe
from django.views.generic.edit import CreateView

import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor

from django_tables2_datatables import tables as dtd_tables
from helpers import url_add_app, render_thisapp
import user_list_uri.views
from user_list_uri.models import List
import user_user_groups.views
from user_user_groups.models import UserGroup
from .models import Issue

N_ISSUES_SERVER = 100
ITEMS_PER_PAGE = 100
ORDER_BY = '-creation_date'
FILTER_USER_LIST_NAME = 'ul' #user list filter table: "<input name="'+FILTER_URI_LIST_NAME+'">"
FILTER_URI_LIST_NAME = 'il' #uri list filter table: "<input name="'+FILTER_URI_LIST_NAME+'">"
FILTER_SERVER_FORM_ID = 'filter-server' #in the form that gets server data: <form id="'+FILTER_SERVER_FORM_ID+'">

def get_issue_table(
        data,
        table_attrs={}
    ):
    custom_table_attrs={'id':'issue-table'}
    custom_table_attrs.update(custom_table_attrs)

    class T(dtd_tables.Datatable):

        id = dtd_tables.LinkColumn(
            url_add_app('detail'),
            args=[A('pk')],
        )

        #TODO: must hack LinkColumn to accept external links...
        #uri = dtd_tables.LinkColumn(
            #url_add_app('detail'),
            #args=[A('pk')],
        #)

        creator = dtd_tables.LinkColumn(
            'userena_profile_detail',
            args=[A('creator.username')],
        )

        class Meta(dtd_tables.Meta):

            model = Issue

            fields = (
                'title',
                'creation_date',
                'uri',
            )

            sequence = [
                'id',
                'creator',
                'title',
                'uri',
                'creation_date',
            ]

        Meta.attrs['id'] = custom_table_attrs['id']

    return T(data)

@require_safe
def index_all(request):
    """lists of issues
    
    get params
    ==========

    - FILTER_URI_LIST_NAME

        only uris in one of the given pk of uri lists will be gotten from server

        can be used multiple times

        Example:

            FILTER_URI_LIST_NAME='ul'

            ul=123&ul456

            only issues with uris inside lists with pks 123 or 456 will be selected

        if none is given, then all issues are selected
    """

    all_items_db = Issue.objects.order_by(ORDER_BY)

    #get_items_form = GetIssuesForm(request.GET)
    #if form.is_valid():
        #nItems = get_items_form.cleaned_data['n']
    #else:
        #nItems = N_items_SERVER
    #selected_items = all_items_db[:nItems]

    #filter by user lists
    filter_user_lists_pk = map(int,request.GET.getlist(FILTER_USER_LIST_NAME))
    filter_usernames = []
    for filter_user_list_pk in filter_user_lists_pk:
        list = get_object_or_404(UserGroup, pk=filter_user_list_pk)
        users_in_group = list.useringroup_set.all()
        filter_usernames.extend( user_in_group.user.username for user_in_group in users_in_group )

    user_list_table = user_user_groups.views.get_user_list_table(
        UserGroup.objects.filter(owner=request.user.pk).order_by(ORDER_BY),
        has_owner=False,
        has_selection=True,
        form=FILTER_SERVER_FORM_ID,
        id='user-lists-table',
        selection_args =
        {
            'name':FILTER_USER_LIST_NAME,
            'accessor':'pk',
            'selected_values':filter_user_lists_pk,
        },
    )

    #filter by uri lists
    filter_uri_lists_pk = map(int,request.GET.getlist(FILTER_URI_LIST_NAME))
    filter_uris = []
    for filter_uri_list_pk in filter_uri_lists_pk:
        list = get_object_or_404(List,pk=filter_uri_list_pk)
        uris_in_group = list.item_set.all()
        filter_uris.extend( uri_in_group.uri for uri_in_group in uris_in_group )
        
    uri_list_table = user_list_uri.views.get_list_table(
        List.objects.filter(owner=request.user.pk).order_by(ORDER_BY),
        has_owner=False,
        has_selection=True,
        form=FILTER_SERVER_FORM_ID,
        id='uri-lists-table',
        selection_args={
            'name':FILTER_URI_LIST_NAME,
            'accessor':'pk',
            'selected_values':filter_uri_lists_pk,
        },
    )

    #get issues table
    selected_issues = Issue.objects.all()
    if filter_usernames:
        selected_issues = selected_issues.filter(creator__username__in=filter_usernames)
    if filter_uris:
        selected_issues = selected_issues.filter(uri__in=filter_uris)
    table = get_issue_table(
        selected_issues
    )

    return render_thisapp(
        request,
        'index_all',
        {
            'n_items_db': all_items_db.count(),
            'table': table,
            'uri_list_table': uri_list_table,
            'user_list_table': user_list_table,
        },
    )

@require_safe
def detail(request, pk):

    issue = get_object_or_404(Issue, pk=pk)

    return render_thisapp(
        request,
        'detail',
        {
            'issue': issue,
        },
    )

class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = (
            'title',
            'uri',
            'description',
        )

@require_http_methods(["GET","HEAD","POST"])
@login_required
def create_issue(request):
    if request.method == "POST":
        form = IssueForm(request.POST)
        if form.is_valid():
            Issue.objects.create(
                creator=request.user,
                title=form.cleaned_data['title'],
                uri=form.cleaned_data['uri'],
                description=form.cleaned_data['description'],
            )
            return HttpResponseRedirect(reverse(
                url_add_app('index_all'),
            ))
    else:
        form = IssueForm()
    return render_thisapp(
        request,
        'create_issue',
        {
            "form": form,
        },
    )

#class IssueCreate(CreateView):
    #model = Issue
    #template_name = 'issue_tracker/create_issue.html'

#create_issue = login_required(IssueCreate.as_view())
