from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from ...tests import create_test_user_groups

class Command(BaseCommand):
    args = '[<groups_per_user> [<users_per_groups>]]'
    help = 'makes test user groups. default: 3 groups per user, 3 users per group'

    def handle(self, groups_per_user=3, users_per_group=3, *args, **options):
        create_test_user_groups(groups_per_user, users_per_group, *args, **options)
