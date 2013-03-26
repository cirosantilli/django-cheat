from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

from ...tests import delete_all_issues

class Command(BaseCommand):
    help = 'deletes all issues'

    def handle(self, *args, **options):
        delete_all_issues()
