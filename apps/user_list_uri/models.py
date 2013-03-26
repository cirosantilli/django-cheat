"""
- User owns lists
- lists hold items
- lists get unique ids per user
"""

import re
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

MAX_ID2_LENGTH = 255
MAX_DESCRIPTION_LENGTH = 2**16-1 #max mysql BLOB TEXT 8kb = 65k
VALID_ID2_RE = r'^[a-z0-9_]+$'
MAX_URI_LENGTH = 255

def validate_id2_chars(id2):
    if not re.match(VALID_ID2_RE,id2):
        raise forms.ValidationError(
            _("groupname \"%s\" contains invalid characters."\
            " valid characters are: 'a' to 'z' (lowercase) and underscore '_'"%(id2))
        )

class List(models.Model):

    owner = models.ForeignKey(
        User,
    )

    id2 = models.CharField(
        'id',
        max_length=MAX_ID2_LENGTH,
        validators=[
            validate_id2_chars,
        ],
        help_text='allowed chars: "[a-z][0-9]_". max length: 255 chars',
    )

    creation_date = models.DateTimeField(
        'created',
        default=lambda:now(),
    )

    description = models.TextField(
        'description',
        max_length=MAX_DESCRIPTION_LENGTH,
        blank=True,
        help_text='max length: %d chars'%MAX_DESCRIPTION_LENGTH,
    )

    def item_count(self):
        return Item.objects.filter(list=self).count()

    def __unicode__(self):
        return self.id2

    class Meta:
        unique_together = ("owner", "id2")

class Item(models.Model):

    list = models.ForeignKey(
        List,
    )

    date_added = models.DateTimeField(
        'added',
        default=lambda:now(),
    )

    uri = models.CharField(
        'uri',
        max_length=MAX_URI_LENGTH,
        blank=True,
    )

    def __unicode__(self):
        return self.user.username
