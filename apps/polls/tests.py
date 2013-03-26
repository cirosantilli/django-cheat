from datetime import datetime

from django.core.urlresolvers import reverse

from django.test import TestCase
from django.test.client import Client

from models import Poll, Choice
from django.contrib.auth.models import User

#to give permissions
    #u = User...
    #u.user_permissions.add(Permission.objects.get(codename='can_vote'))
    #u.save

class PollTest(TestCase):

    def setUp(self):

        #users
        self.users = [
                User.objects.create(username='user0',password='pass0'),
                User.objects.create(username='user1',password='pass1'),
                ]

        #polls
        now = datetime.now()
        self.polls = [
                Poll.objects.create(question='question0', pub_date=now),
                Poll.objects.create(question='question1', pub_date=now)
                ]

        self.choices = [
                Choice.objects.create(poll=self.polls[0], choice_text="question0", votes=0),
                Choice.objects.create(poll=self.polls[0], choice_text="question1", votes=0),
            ]

    def test_models(self):
        # Issue a GET request.
        response = self.client.get(reverse('poll_index'))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


