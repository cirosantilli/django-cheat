import re
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

MAX_ID2_LENGTH = 255
VALID_ID2_RE = r'^[a-z0-9_]+$'

def validate_id2_chars(id2):
    if not re.match(VALID_ID2_RE,id2):
        raise forms.ValidationError(
            _("groupname \"%s\" contains invalid characters."\
            " valid characters are: 'a' to 'z' (lowercase) and underscore '_'."%(id2))
        )

class UserGroup(models.Model):

    owner = models.ForeignKey(
        User,
    )

    id2 = models.CharField(
        'id',
        max_length=MAX_ID2_LENGTH,
        validators=[
            validate_id2_chars,
        ],
    )

    creation_date = models.DateTimeField(
        'created',
        default=lambda:now(),
    )

    def __unicode__(self):
        return self.id2

    class Meta:
        unique_together = ("owner", "id2")

class UserInGroup(models.Model):

    user = models.ForeignKey(
        User,
        #related_name='users'
    )

    date_added = models.DateTimeField(
        'added',
        default=lambda:now(),
    )

    group = models.ForeignKey(
        UserGroup,
        #related_name='group',
    )

    def __unicode__(self):
        return self.user.username


