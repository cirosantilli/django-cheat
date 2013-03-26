"""creates a test db for this app"""

from django.core.management.base import BaseCommand, CommandError

from accounts.tests import create_test_users, delete_all_users
from user_user_groups.tests import create_test_user_groups
from user_list_uri.tests import create_test_uri_lists
from issue_tracker.tests import create_test_issues

uris = [
    'https://github.com/cirosantilli/elearn/blob/master/main.tex#introduction',
    'https://github.com/cirosantilli/elearn/blob/master/main.tex#conclusion',
    'https://github.com/cirosantilli/elearn/blob/master/main.bib',
    'https://github.com/cirosantilli/elearn/blob/master/main.sty',
    'isbn:0123456789?pg=15',
    'isbn:0123456789?pg=30',
    'isbn:9876543210',
]

class Command(BaseCommand):

    help = 'clears the database and creates test data'

    def handle(self, item_per_user=3, *args, **options):
        delete_all_users()
        create_test_users(nusers=10)
        create_test_user_groups(
            groups_per_user=3,
            users_per_group=3,
        )
        create_test_uri_lists(
            uri_lists_per_user=3,
            max_uris_per_uri_list=5,
            uris=uris,
        )
        create_test_issues(
            issues_per_user=3,
            uris=uris
        )
