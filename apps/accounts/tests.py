"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import sys

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Profile

def create_test_users(nusers, *args, **options):

        users = []

        #create admin
        u = User.objects.create_user("admin","admin@mail.com","pass")
        u.is_superuser=True
        u.is_staff=True
        u.save()
        users.append(u)

        #create other useres
        for i in xrange(nusers):
            u = User.objects.create_user("user%d"%i,"user%d@mail.com"%i,"pass")
            u.save()
            users.append(u)

        for user in users:
            Profile.objects.create(user=user)

        sys.stderr.write("created one superuser and %d regular users\n" % (nusers))

def delete_all_users():
    for user in User.objects.all():
        user.delete() #also call delete on choices, default of foreign key!

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


