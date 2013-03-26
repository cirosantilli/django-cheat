from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from polls.models import Poll

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'deletes the specified polls'

    def handle(self, *args, **options):
        for poll_id in args:
            try:
                poll = Poll.objects.get(pk=int(poll_id))
            except Poll.DoesNotExist:
                raise CommandError('poll "%s" does not exist' % poll_id)

            poll.delete() #also deletes choices because of foreign key magic!
            self.stderr.write('Successfully deleted poll "%s"' % poll_id)


