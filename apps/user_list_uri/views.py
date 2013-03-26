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
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods, require_safe

import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor

from user_list_uri.models import List, Item
from django_tables2_datatables import settings as dtd_settings, tables as dtd_tables
from helpers import url_add_app, render_thisapp

ITEMS_PER_PAGE = 100
ORDER_BY = 'id2'

def get_list_table(
        data,
        has_owner=True,
        has_selection=True,
        selection_args={},
        form='issue-lists-bulk-action',
        id='list-table',
    ):
    """returns an instance of a class derived from tables.Table

    :param owner: user that the table links to
    :type owner: django.contrib.auth.models.User
    :param data: data, same as passed to django_tables2.Table constructor
    :returns: the table that links to owner's user groups
    :param selection_args: custom arguments be passedto dtd_tables.MasterCheckBoxColumn

        default:

        custom_selection_args = {
            'master_group':'select-group',
            'name':'id2',
            'accessor':'id2',
        }

        form=form is also passed

    :type selection_args: dict
    :rtype: django_tables2.Table instance
    """

    custom_selection_args = {
        'master_group':'uri-list-select',
        'name':'id2',
        'accessor':'id2',
    }
    custom_selection_args.update(selection_args)

    class T(dtd_tables.Datatable):

        if has_selection:
            selection = dtd_tables.MasterCheckBoxColumn(
                form=form,
                **custom_selection_args
            )

        if has_owner:
            owner = dtd_tables.LinkColumn(
                'userena_profile_detail',
                args=[A('owner.username')],
                #'_detail',
                #args=[A('owner.username'),A('id2')],
            )

        id2 = dtd_tables.LinkColumn(
            url_add_app('detail'),
            args=[A('owner.username'),A('id2')],
        )

        class Meta(dtd_tables.Meta):
            model = List
            fields = (
                'creation_date',
                'item_count'
            )

            sequence = []
            if has_selection:
                sequence.append('selection')
            if has_owner:
                sequence.append('owner')
            sequence.extend([
                'id2',
                'item_count',
                'creation_date',
            ])
        Meta.attrs["id"] = id

    t = T(data)
    setattr(t,'bulk_form_id',form)
    return t

@require_safe
def index_all(request):
    """lists of all users"""

    all_items_db = List.objects.all().order_by(ORDER_BY)

    table = get_list_table(
        all_items_db,
        has_owner=True,
        has_selection=True,
        form='bulk',
    )

    return render_thisapp(
        request,
        'index_all',
        {
            'total_items_db': all_items_db.count(),
            'table': table,
        },
    )

@require_safe
def index_user(request, owner_username):
    """lists of a given owner"""

    owner = get_object_or_404(User,username=owner_username)
    all_items_db = List.objects.filter(owner=owner).order_by(ORDER_BY)

    table = get_list_table(
        all_items_db,
        has_selection=True,
        has_owner=False,
        form='bulk',
    )

    return render_thisapp(
        request,
        'index_user',
        {
            'owner': owner,
            'total_items_db': all_items_db.count(),
            'table': table,
        },
    )

def get_item_table(
        data,
        id='',
        form='',
        has_selection=True,
    ):
    """returns an instance of a class named UserTable derived from tables.Table

    :param data: table data
    :type data: data accepted by a django_tables2.Table constructor
    :param id: <table id="id">
    :type id: string
    :param form: <td><input form="form">
    :type form: string
    :param has_selection: if True, table gets a master checkbox column at right
    :type has_selection: boolean
    """

    class T(dtd_tables.Datatable):

        if has_selection:
            selection = dtd_tables.MasterCheckBoxColumn(
                "select-users",
                name="usernames",
                form=form,
                accessor="username",
            )

        class Meta(dtd_tables.Meta):

            model = Item

            fields = (
                'uri',
                'date_added',
            )

            sequence = []
            if has_selection:
                sequence.append('selection')
            sequence.extend([
                'uri',
                'date_added',
            ])

        Meta.attrs['id'] = id

    return T(data)

@require_safe
def detail(request, owner_username, id2):

    owner = get_object_or_404(User, username=owner_username)
    list = get_object_or_404(List, owner=owner, id2=id2)
    all_items_db = Item.objects.filter(list=list).order_by('uri')

    table = get_item_table(
        all_items_db,
        id='items',
        form='bulk',
        has_selection=False,
    )

    return render_thisapp(
        request,
        'detail',
        {
            'owner': owner,
            'list': list,
            'total_items_db': all_items_db.count(),
            'table': table,
        },
    )

class UrisField(forms.Field):
    """to preprocess form data, make this new class
    
    validated data will always be a list of strings split at \n or \r chars
    and such that:

    1) only one copy is kept of dupe lines
    2) whiteline only lines are discarded
    """
    def to_python(self, value):
        """
        >>> "a\nb\rc\n\r\r\rd"
        ["a","b","c","d"]
        >>> "b\na"
        ["a","b"]
        >>> "a\na"
        ["a"]
        >>> "a\n "
        ["a"]
        """
        if not value:
            return []
        return list(set(sorted(filter(lambda v:v.strip(),value.splitlines()))))

#TODO 0 add help
class ListForm(ModelForm):

    uris = UrisField(
        widget=forms.Textarea(),
        required=False,
        help_text='newline separated uris. whitechar lines ignored. dupes will be removed'
    )

    def __init__(self, *args, **kwargs):
        """
        :param owner:
            Auth.User object

            if no owner is given, unicity check does nothing:
            it is supposed by clean that this is the initial GET request.

            rationale: without a owner, one cannot know if the
            id2/owner_username pair is unique.

        :param old_id2:
            String

            if given supposes it is an update of old_id2.
            therefore, in that case, will only raise an unicity check error
            it then new username/id2 is already taken and if the
            new groupaname is different from the old one, meaning that the
            user is trying to update the name to a new one.

        :param instance:
            same as super class instance, except this is also used to set initial data for
            the uris textarea. therefore there is no need to user the initial
            kwarg to do this:
            
            >>> owner = get_object_or_404(User, username=owner_username)
            >>> list = get_object_or_404(List, owner=owner, id2=id2)
            >>> form = ListForm(instance=list)

            and the initial['uris'] textarea will automatically get populated

            if initial['uris'] is specified, it overides this automatic initialization
        :type instance: List
        """

        self.owner = kwargs.pop('owner',None)
        self.old_id2 = kwargs.pop('old_id2',None)

        #update initial values based on model
        instance = kwargs.get('instance',None)
        set_initial_uris = False
        if instance: 
            initial = kwargs.get('initial',{})
            if initial:
                uris = initial.get('uris','')
                if not uris: #
                    set_initial_uris = True
            else:
                kwargs['initial'] = {}
                set_initial_uris = True

        #at this point, kwargs['initial'] is assured to exist
        if set_initial_uris:
            kwargs['initial']['uris'] = "\n".join( item.uri for item in instance.item_set.all() )

        super(ListForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        ensure owner/id2 pair is unique taking into consideration update
        """
        cleaned_data = super(ListForm, self).clean()

        if self.owner: #only for POST
            new_id2 = cleaned_data.get('id2',None)
            if new_id2:
                if List.objects.filter(
                            owner=self.owner,
                            id2=new_id2
                        ).exists(): #new name exists: might be error
                    error = False
                    if( (self.old_id2 and self.old_id2 != new_id2 ) #update, and name different from old. error
                            or not self.old_id2 ): #create and new name exists. error
                        self._errors['id2'] = [_(
                                "groupaname \"%s\" already exists for user \"%s\". "
                                "please choose a different groupname."
                                %(new_id2,self.owner.username)
                            )]
        return cleaned_data

    class Meta:
        model = List
        fields = (
            'id2',
            'description',
            'uris',
        )

#TODO 0 confirm before exiting create!
#TODO 1 add nice admin search widget
@require_http_methods(["GET","HEAD","POST"])
@login_required
def create_list(request, owner_username):

    owner = get_object_or_404(User, username=owner_username)

    if request.user != owner:
        return HttpResponse(_(
            "you are logged in as \"%s\" "
            "and cannot create a group for user \"%s\""
            % (request.user.username, owner.username)
        ))

    if request.method == "POST":
        form = ListForm(request.POST, owner=owner)
        if form.is_valid():
            uri_list = List.objects.create(
                owner=owner,
                id2=form.cleaned_data['id2'],
                description=form.cleaned_data['description'],
            )
            for uri in form.cleaned_data['uris']:
                Item.objects.create(
                    list=uri_list,
                    uri=uri,
                )
            return HttpResponseRedirect(reverse(
                url_add_app('index_user'),
                args=(owner_username,),
            ))
    else:
        form = ListForm()

    return render_thisapp(
        request,
        'create_list',
        {
            "form": form,
            "owner": owner,
        },
    )

@require_http_methods(["GET","POST"])
@login_required
def update_list(request, owner_username, id2):

    owner = get_object_or_404(User, username=owner_username)
    list = get_object_or_404(List, owner=owner, id2=id2)

    if request.user != owner:
        return HttpResponse(_(
            "you are logged in as \"%s\" "
            "and cannot update a data for another user \"%s\""
            % (request.user.username, owner.username)
        ))

    if request.method == "POST":

        #load post data on form so in case validation fails it will be redirected here
        form = ListForm(
            request.POST,
            owner=owner,
            old_id2=list.id2
        )
        if form.is_valid():

            #update id2
            new_id2 = form.cleaned_data['id2']
            if new_id2 != list.id2: #validation already guarantees new name is available
                list.id2 = new_id2
                list.save()

            #update description
            new_description = form.cleaned_data['description']
            if new_description != list.description:
                list.description = new_description
                list.save()

            #update uris
            old_items = list.item_set.all()
            old_uris = [ item.uri for item in old_items ]
            new_uris = form.cleaned_data['uris']

            #add new ones
            for new_uri in new_uris:
                if not new_uri in old_uris:
                    Item.objects.create(
                        uri=new_uri,
                        list=list,
                    )

            #delete removed ones
            for old_uri in old_uris: 
                if not old_uri in new_uris:
                    next( item for item in old_items if item.uri==old_uri ).delete()

            return HttpResponseRedirect(reverse(
                url_add_app('detail'),
                args=(owner_username,list.id2)
            ))
    else:
        form = ListForm(instance=list)

    return render_thisapp(
        request,
        'update_list',
        {
            'form': form,
            'owner': owner,
            'list': list,
            #'update_table': update_table,
            #'update_table_filter': update_table_filter,
        },
    )

#TODO are you sure you want to delete?
@login_required
@require_http_methods(["POST"])
def delete_selected(request, owner_username):
    """
    delete multiple groups given in post request

    owner_username is given on the url

    id2 to delete for the given owner_username
    are given in request.POST.getlist['id2']

    if a single owner_username groupname pair does not exist,
    no deletion is made, and a 404 is returned
    """

    owner = get_object_or_404(User, username=owner_username)

    if request.user != owner:
        return HttpResponse(_("you cannot delete a group that belongs to another user")) #TODO decent

    #first check all id2 exist, then delete them
    #if one does not exist, 404
    groups = [ get_object_or_404(List, owner=owner, id2=id2)
            for id2 in request.POST.getlist('id2') ] 

    for group in groups:
        group.delete()

    return HttpResponseRedirect(reverse(
        url_add_app('index_user'),
        args=(owner_username,),
    ))

def _get_unique_id2(user, id2):
    """
    returns an id2 such that the pair user/id2 is not taken up

    if no conflict exists for id2, returns the given id2
    
    else "000_\n+_" preffix is appended to the id2, where \n+ is
    the first integer starting from 1 that makes the id2 unique
    """
    PREFIX = '000_'
    SUFFIX = '_'
    if ( List.objects.filter(
                owner=user,
                id2=id2,
            ).exists() ):
        i=1
        old_id2 = id2
        id2 = PREFIX + str(i) + SUFFIX + old_id2
        while ( List.objects.filter(
                    owner=user,
                    id2=id2,
                ).exists() ):
            i=i+1
            id2 = PREFIX + str(i) + SUFFIX + old_id2
    return id2

@login_required
@require_http_methods(["POST"])
def copy_selected(request, owner_username):
    """
    same as delete, but copies the groups from the given owner_username,
    to the authenticated user.

    in case of conflict of existing id2,
    it is resolved by _get_unique_id2
    """

    owner = get_object_or_404(User, username=owner_username)

    lists = [ get_object_or_404(List, owner=owner, id2=id2)
            for id2 in request.POST.getlist('id2') ] 

    for old_list in lists:
        new_list = List.objects.create(
            owner=request.user,
            id2=_get_unique_id2(request.user,old_list.id2)
        )
        for user_in_list in Item.objects.filter(list=old_list):
            user_in_list.pk = None
            user_in_list.list = new_list
            user_in_list.save()

    return HttpResponseRedirect(reverse(
        url_add_app('index_user'),
        args=(owner_username,)
    ))

@login_required
@require_http_methods(["POST"])
def bulk_action(request, owner_username):
    """
    decides between bulk actions (actions which may affect several objects at once)
    such as copy or delete.
    """

    if request.POST.__contains__('copy'):
        return copy_selected(request,owner_username)
    if request.POST.__contains__('delete'):
        return delete_selected(request,owner_username)
    else:
        return HttpResponseBadRequest("unknown action" % action)

#if __name__ == "__main__":
    #quick and dirty tests
    #import doctest
    #doctest.testmod()


