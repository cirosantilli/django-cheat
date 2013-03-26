from datetime import datetime
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from ...tests import create_test_uri_lists

class Command(BaseCommand):
    args = '[<item2_per_user> [<item3_per_item2>]]'
    help = 'makes test user groups. default: 3 groups per user, 3 users per group'

    def handle(self, uri_lists_per_user=3, max_uris_per_uri_list=5, *args, **options):
        create_test_uri_lists(
            uri_lists_per_user,
            max_uris_per_uri_list,
        )
