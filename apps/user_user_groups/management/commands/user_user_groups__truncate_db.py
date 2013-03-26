from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from ...tests import delete_all_user_groups

class Command(BaseCommand):
    help = 'deletes all lists and their items'

    def handle(self, *args, **options):
        delete_all_user_groups()
