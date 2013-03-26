"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import sys

from django.contrib.auth.models import User
from django.test import TestCase

from .models import List, Item

def create_test_uri_lists(
        uri_lists_per_user=3,
        max_uris_per_uri_list=5,
        uris=[],
    ):
    """
    :param uris: uris to give to users.

        uris are taken sequentially from this list, continue from the
        last given url, even if it was given to a different user. Example:

            uri_lists_per_user = 2
            uris_per_uri_list = 2
            uris = ['u1','u2','u3']
            users = ['s1','s2']

            s1:
                l1:
                    u1 u2
                l2:
                    u3 u1
            s2:
                l1:
                    u2 u3
                l2:
                    u1 u2

        default value:

            xrange( (User.objects.count()*uri_lists_per_user*uris_per_uri_list/3)+1 )

    :type uris: list of strings
    """

    owners = User.objects.order_by('username')

    if not uris:
        uris = [
            "uri%d"%i for i in
            xrange( (owners.count()*uri_lists_per_user*max_uris_per_uri_list/3)+1 )
        ]

    urin = 0
    uris_per_uri_list = 0
    for owner in owners:
        for i in xrange(uri_lists_per_user):
            list = List.objects.create(
                owner=owner,
                id2="id%d"%i,
                description="desc%d"%i,
            )
            for j in xrange(uris_per_uri_list):
                Item.objects.create(
                    list=list,
                    uri=uris[urin],
                )
                urin = (urin+1)%len(uris)
            uris_per_uri_list = (uris_per_uri_list+1) % max_uris_per_uri_list

    sys.stderr.write(
        "created %d uri lists per user with %d uris per list\n"
        % (uri_lists_per_user, uris_per_uri_list)
    )

def delete_all_uri_lists():
    for user in List.objects.all():
        user.delete()

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
