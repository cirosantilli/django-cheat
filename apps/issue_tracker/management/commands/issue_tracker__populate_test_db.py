from django.contrib.auth.models import User, Permission

from django.core.management.base import BaseCommand, CommandError

from ...tests import create_test_issues

class Command(BaseCommand):
    args = '[<item_per_user>]'
    help = 'makes test user groups. default: 3 groups per user, 3 users per group'

    def handle(self, issues_per_user=3, *args, **options):
        create_test_issues(issues_per_user)
