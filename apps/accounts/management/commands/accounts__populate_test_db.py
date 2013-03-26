from datetime import datetime
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from ...tests import create_test_users

class Command(BaseCommand):
    args = '[<nusers>]'
    help = 'makes test users and their profiles. default: 10 users'

    def handle(self, nusers=10, *args, **options):
        create_test_users(nusers, *args, **options)
