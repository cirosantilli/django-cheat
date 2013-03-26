from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from polls.models import Poll

class Command(BaseCommand):
    help = 'deletes all polls'

    def handle(self, *args, **options):
        for poll in Poll.objects.all():
            poll.delete() #also call delete on choices, default of foreign key!


