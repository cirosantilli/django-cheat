from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User

from ...tests import delete_all_uri_lists

class Command(BaseCommand):
    help = 'deletes all Users'

    def handle(self, *args, **options):
        delete_all_uri_lists()
