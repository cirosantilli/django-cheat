from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

from datetime import datetime

class Poll(models.Model):
    question = models.CharField(
            'question',
            max_length=200
        )
    pub_date = models.DateTimeField(
            'date published',
            default=lambda:datetime.now()
        )

    creator = models.ForeignKey(User, related_name='creator')

    users_who_voted = models.ManyToManyField(User)
    #stores which users voted for which polls
    #ManyToManyField creates a new table, and therefore makes effiecient relational querries!

    def has_user_voted(self,user):
        """
        Return True iff the user has already voted
        """
        return Poll.objects.filter(
                id=self.id,
                users_who_voted__id=user.id
            ).count() > 0

    def set_user_has_voted(self,user):
        """
        Tells poll that the user has voted
        """
        self.users_who_voted.add(user)
        self.save()

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'pub_date' #if clicks on this, sorts by r2 instead (gives the same thing, but sort by function is not supported)
    was_published_recently.boolean = True #treats output as boolean, and prints nice output to end user
    was_published_recently.short_description = 'published recently?' #title that will to to admin colum

    def __unicode__(self):
        #analogous to str(), but unicode
        #str() calls this
        #this output may be printed to end users
        return self.question

    class Meta:
            permissions = (
                ("can_view", "can see a given poll"),
                ("can_vote", "can vote for a given poll"),
            )

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField()

    def __unicode__(self):
            return self.choice_text


