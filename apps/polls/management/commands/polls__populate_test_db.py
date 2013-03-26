import itertools

from datetime import datetime
from optparse import make_option
from django.contrib.auth.models import User

from django.core.management.base import BaseCommand, CommandError

from polls.models import Poll, Choice

class Command(BaseCommand):
    args = '[<npolls> [<choices_per_poll>]]'
    help = 'makes a bunch of test polls.\n\n create_test_polls npolls choices_per_poll'

    def handle(self, npolls=50, choices_per_poll=3, *args, **options):

        npolls = int(npolls)
        choices_per_poll = int(choices_per_poll)

        users = User.objects.all()
        nusers = User.objects.count()

        now = datetime.now()
        polls = [
                    Poll.objects.create(
                            question='question%d' % i,
                            pub_date=now,
                            creator=users[i%nusers]
                    )
                    for i in xrange(npolls)
                ]
        
        for i,j in itertools.product(xrange(npolls),xrange(choices_per_poll)):
            Choice.objects.create(poll=polls[i], choice_text="choice%d" % j, votes=0)

        self.stderr.write("created %d polls, with %d choices per poll" % (npolls, choices_per_poll))


