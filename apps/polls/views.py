from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import inlineformset_factory
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django import forms

from polls.models import Choice, Poll

##without generic templates:

#def index(request):
    #latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
        #t = loader.get_template('polls/index.html')
        #c = Context({
            #'latest_poll_list': latest_poll_list,
        #})
        #return HttpResponse(t.render(c))

#shortcut to the above

ITEMS_PER_PAGE = 100

def index(request):
    items_list = Poll.objects.all().order_by('-pub_date')
    paginator = Paginator(items_list, POLLS_PER_PAGE)

    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)

    return render(
            request,
            'polls/index.html',
            {
                'items': items
            },
            )

#def detail(request, id):
    #p = get_object_or_404(Poll, pk=id)
    #return render_to_response('polls/detail.html', {'poll': p})

#def results(request, poll_id):
    #p = get_object_or_404(Poll, pk=poll_id)
    #return render_to_response('polls/results.html', {'poll': p})

#class PollForm(forms.Form):
    #question = forms.CharField(max_length=256)

class PollForm(forms.ModelForm):

    class Meta:
        model = Poll
        fields = (
                'question',
            )
        #exclude = () #what to exclude instead


#class ChoiceForm(forms.ModelForm):

    #class Meta:
        #model = Choice
        #fields = ('choice_text',)

MAX_INGREDIENTS = 20

ChoiceFormSet = inlineformset_factory(Poll, 
    Choice, 
    can_delete=False,
    extra=MAX_INGREDIENTS)

@login_required #if not, go to login page
def create(request):
    if request.method == 'POST': # If the form has been submitted...
        form = PollForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            question = form.cleaned_data['question']
            Poll.objects.create(question=question, creator=request.user)
            return HttpResponseRedirect(reverse('poll_index')) # Redirect after POST
    else:
        form = PollForm() # An unbound form

    return render(
            request,
            'polls/create.html',
            {
                'form': form,
            },
            )

#@permission_required('polls.can_vote') #simplified user_passes_test for single db permission
#@user_passes_test(lambda u: u.has_perm('polls.can_vote', login_url=None)) #if not go to login_url page
@login_required #if not, go to login page
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render_to_response('polls/detail.html', {
            'poll': poll,
            'error_message': "you didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
        if request.user.is_authenticated():
            if request.user.has_perm('polls.can_vote'):
                if not poll.has_user_voted(request.user):
                    selected_choice.votes += 1
                    selected_choice.save()
                    poll.set_user_has_voted(request.user)
                    return HttpResponseRedirect(reverse('poll_results', args=(poll.id,)))
                return HttpResponse('you have already voted once, cheater!')
            else:
                return HttpResponse('you dont have permission to vote for polls')
        else:
            return HttpResponse('you must be logged in to vote')


