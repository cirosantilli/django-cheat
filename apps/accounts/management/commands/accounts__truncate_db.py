from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from ...tests import delete_all_users

class Command(BaseCommand):
    help = 'deletes all Users'

    def handle(self, *args, **options):
        delete_all_users()
