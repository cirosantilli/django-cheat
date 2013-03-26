from django.conf import settings

import os

THISAPP = os.path.split(os.path.dirname(os.path.abspath(__file__)))[1]

MASTER_GROUP_ATTR = getattr(settings,
        THISAPP+'_MASTER_CHECKBOX_GROUP_ATTR',
        'master-group',
    )

SLAVE_GROUP_ATTR = getattr(settings,
        THISAPP+'_SLAVE_CHECKBOX_GROUP_ATTR',
        'slave-of',
    )

CONTEXT = {
    'master_checkbox_group_attr':MASTER_GROUP_ATTR,
    'slave_checkbox_group_attr':SLAVE_GROUP_ATTR,
}


