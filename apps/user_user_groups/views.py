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
from django.forms.widgets import CheckboxSelectMultiple
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods, require_safe

import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor

from user_user_groups.models import UserGroup, UserInGroup
from django_tables2_datatables import settings as dtd_settings, tables as dtd_tables
from settings import THISAPP

ITEMS_PER_PAGE = 100

def get_user_list_table(
        data,
        has_owner=True,
        has_selection=True,
        selection_args={},
        form='user-list-bulk-action',
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
        'master_group':'select-group',
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
                #THISAPP+'_index_user',
                #args=[A('owner.username'),A('id2')],
            )

        id2 = dtd_tables.LinkColumn(
            THISAPP+'_detail',
            args=[A('owner.username'),A('id2')],
        )

        usercount = tables.Column(
            accessor="useringroup_set.count",
            verbose_name="item count",
        )

        class Meta(dtd_tables.Meta):
            model = UserGroup
            fields = (
                'creation_date',
            )

            sequence = []
            if has_selection:
                sequence.append('selection')
            if has_owner:
                sequence.append('owner')
            sequence.extend([
                'id2',
                'usercount',
                'creation_date',
            ])
        Meta.attrs["id"] = id

    t = T(data)
    setattr(t,'bulk_form_id',form)
    return t

def index_all(request):
    """item2 of all owners"""

    all_items_db = UserGroup.objects.all().order_by('id2')

    table = get_user_list_table(
        all_items_db,
        has_owner=True,
        has_selection=True,
        form='bulk-action',
    )

    return render(
        request,
        THISAPP+'/index_all.html',
        {
            'total_items_db': all_items_db.count(),
            'table': table,
        },
    )

@require_safe
def index_user(request, owner_username):
    """itmes2 of a given owner"""

    owner = get_object_or_404(User,username=owner_username)
    all_items_db = UserGroup.objects.filter(owner=owner).order_by('id2')

    table = get_user_list_table(
        all_items_db,
        has_selection=True,
        has_owner=False,
        form='bulk-action',
    )

    return render(
        request,
        THISAPP+'/index_user.html',
        {
            'owner': owner,
            'total_items_db': all_items_db.count(),
            'table': table,
        },
    )

def get_item3_table(
        data,
        id='',
        form='',
        has_selection=True,
    ):
    """returns an instance of a class derived from tables.Table,
    containing item3 data

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

        username = dtd_tables.LinkColumn(
            'userena.views.profile_detail',
            accessor="user.username",
            args=[A('user.username')],
        )

        class Meta(dtd_tables.Meta):

            model = UserInGroup

            fields = (
                'date_added',
            )

            sequence = []
            if has_selection:
                sequence.append('selection')
            sequence.extend([
                'username',
                'date_added',
            ])

        Meta.attrs['id'] = id

    return T(data)

@require_safe
def detail(request, owner_username, id2):

    owner = get_object_or_404(User, username=owner_username)
    item2 = get_object_or_404(UserGroup, owner=owner, id2=id2)
    all_items_db = UserInGroup.objects.filter(group=item2).order_by('user__username')

    table = get_item3_table(
        all_items_db,
        id='items',
        form='bulk-action',
        has_selection=False,
    )

    return render(
        request,
        THISAPP+'/detail.html',
        {
            'owner': owner,
            'item2': item2,
            'total_items_db': all_items_db.count(),
            'table': table,
        },
    )

#TODO 0 add help
class Item2Form(ModelForm):

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=CheckboxSelectMultiple(
            attrs={
                'rows':'10',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        """
        #kwargs

        - owner
            Auth.User object

            if no owner is given, unicity check does nothing:
            it is probably the initial GET request.

            rationale: without a owner, one cannot know if the
            id2/owner_username pair is unique.

        - initial_item2
            UserGroup object

            loads form with given UserGroup object.

            if given, dictionnary *arg is ignored,
            just like it is if a ModelForm is given a initial
            kwarg

            if 'initial' is given with initial_item2, its values are considered
            'initial' dictionnary value pairs have precedence over
            those extracted in initial_item2.

        - old_id2
            String

            if given supposes it is an update of old_id2.
            therefore, in that case, will only raise an unicity check error
            it then new username/id2 is already taken and if the
            new groupaname is different from the old one, meaning that the
            user is trying to update the name to a new one.
        """

        self.owner = kwargs.pop('owner',None)
        self.old_id2 = kwargs.pop('old_id2',None)

        #update initial values based on model
        initial_item2 = kwargs.pop('initial_item2',None)
        if initial_item2: 
            old_initial = kwargs.get('initial',{})
            kwargs['initial'] = {}
            kwargs['initial'].update(model_to_dict(initial_item2,fields=['id2']))
            kwargs['initial']['uris'] = [
                item3.user.pk for useringroup in initial_item2.useringroup_set.all()
            ]
            kwargs['initial'].update(old_initial)

        super(Item2Form, self).__init__(*args, **kwargs)

    def clean(self):
        """
        ensure owner/id2 pair is unique taking into consideration update
        """
        cleaned_data = super(Item2Form, self).clean()
        if self.owner: #POST
            new_id2 = cleaned_data.get('id2',None) #because is_valid calls clean first, before passing it to the model for field validation
            if new_id2:
                if UserGroup.objects.filter(
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
        model = UserGroup
        fields = (
                'id2',
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
            "and cannot edit data for user \"%s\""
            % (request.user.username, owner.username)
        ))

    if request.method == "POST":
        form = Item2Form(request.POST, owner=owner)
        if form.is_valid():
            group = UserGroup.objects.create(
                id2=form.cleaned_data['id2'],
                owner=owner,
            )
            for user in form.cleaned_data['users']:
                UserInGroup.objects.create(
                    user=user,
                    group=group,
                )
            return HttpResponseRedirect(reverse(THISAPP+'_index_user',args=(owner_username,)))
    else:
        form = Item2Form()

    return render(
        request,
        THISAPP+"/create_list.html",
        {
            "form": form,
            "owner": owner,
        },
    )

@require_http_methods(["GET","POST"])
@login_required
def update_list(request, owner_username, id2):

    owner = get_object_or_404(User, username=owner_username)
    item2 = get_object_or_404(UserGroup, owner=owner, id2=id2)


    if request.user != owner:
        return HttpResponse(_(
            "you are logged in as \"%s\" "
            "and cannot update a group for user \"%s\""
            % (request.user.username, owner.username)
        ))

    if request.method == "POST":
        form = Item2Form(request.POST, owner=owner, old_id2=item2.id2)
        if form.is_valid():

            #update name
            old_name = item2.id2
            new_name = form.cleaned_data['id2']
            if new_name != old_name: #validation already guarantees new name is available
                item2.id2 = new_name
                item2.save()

            #update users
            old_users = item2.useringroup_set.all()
            new_users = form.cleaned_data['users']
            for user in new_users: #add new ones
                if not user in old_users:
                    item3_in_item2 = UserInGroup.objects.create(
                            user=user,
                            group=item2,
                        )
            for user in old_users: #delete removed ones
                if not user in new_users:
                    user.delete()
            return HttpResponseRedirect(
                    reverse(THISAPP+'_detail',
                    args=(owner_username,item2.id2))
                )
    else:
        all_items_db = UserInGroup.objects.filter(group=item2).order_by('user__username')
        update_form_id = 'update' #<input form=> and <form id=>
        update_table = get_item3_table(
            all_items_db,
            id='update_items',
            form=update_form_id,
        )

        form = Item2Form(initial_item2=item2)

    return render(
        request,
        THISAPP+"/update_list.html",
        {
            'form': form,
            'owner': owner,
            'item2': item2,
            'update_table': update_table,
            'update_form_id': update_form_id,
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
    groups = [ get_object_or_404(UserGroup, owner=owner, id2=id2)
            for id2 in request.POST.getlist('id2') ] 

    for group in groups:
        group.delete()

    return HttpResponseRedirect(reverse(THISAPP+'_index_user',args=(owner_username,)))

def _get_unique_id2(user, id2):
    """
    returns an id2 such that the pair user/id2 is not taken up

    if no conflict exists for id2, returns the given id2
    
    else "000_\n+_" preffix is appended to the id2, where \n+ is
    the first integer starting from 1 that makes the id2 unique
    """
    PREFIX = '000_'
    SUFFIX = '_'
    if ( UserGroup.objects.filter(
                owner=user,
                id2=id2,
            ).exists() ):
        i=1
        old_id2 = id2
        id2 = PREFIX + str(i) + SUFFIX + old_id2
        while ( UserGroup.objects.filter(
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

    groups = [ get_object_or_404(UserGroup, owner=owner, id2=id2)
            for id2 in request.POST.getlist('id2') ] 

    for old_group in groups:
        new_group = UserGroup.objects.create(
            owner=request.user,
            id2=_get_unique_id2(request.user,old_group.id2)
        )
        for item3_in_item2 in UserInGroup.objects.filter(group=old_group):
            item3_in_item2.pk = None
            item3_in_item2.group = new_group
            item3_in_item2.save()

    return HttpResponseRedirect(reverse(THISAPP+'_index_user',args=(owner_username,)))

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


