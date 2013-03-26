"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import sys

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Issue

def create_test_issues(
        issues_per_user=3,
        uris=[]
    ):
    """create test issues
    
    :param uris: uris to assign to issues

        default:

            uris = [ "uri%d"%i for i in xrange(creators.count()*issues_per_user/3) ]
        
    :type uris: list of strings
    """

    creators = User.objects.order_by('username')

    if not uris:
        uris = [ "uri%d"%i for i in xrange(creators.count()*issues_per_user/3) ]
        
    urin = 0
    for creator in creators:
        for i in xrange(issues_per_user):
            uri=uris[urin]
            list = Issue.objects.create(
                creator=creator,
                title="title%d"%i,
                description="desc%d"%i,
                uri=uri
            )
            urin = (urin+1)%len(uris)

    sys.stderr.write(
        "created %d issues per user\n" % (issues_per_user)
    )

def delete_all_issues():
    for issue in Issue.objects.all():
        issue.delete()

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


