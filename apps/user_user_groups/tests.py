import sys
import random

from django.test import TestCase
from django.contrib.auth.models import User

from .models import UserGroup, UserInGroup

def create_test_user_groups(
        groups_per_user=3,
        users_per_group=3,
        *args, **options
    ):

    users = User.objects.order_by('username')
    for owner in users:
        for i in xrange(groups_per_user):
            group = UserGroup.objects.create(
                owner=owner,
                id2="group%d"%i
            )
            for user in random.sample(users, users_per_group):
                user_in_group = UserInGroup.objects.create(
                    user=user,
                    group=group,
                )
                #group.group_set.add(user_in_group)

    sys.stderr.write(
        "created %d groups per user with %d users per group\n"
        % (groups_per_user, users_per_group)
    )

def delete_all_user_groups():
    for usergroup in UserGroup.objects.all():
        usergroup.delete()

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
