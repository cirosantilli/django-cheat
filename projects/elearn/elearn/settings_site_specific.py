"""
contains settings that change with different deployments

this version is for localhost dev

this is done so as to allow simple deployment only using symlinks

files that stay the same with deployments are symliked to a deploy dir (git, ftp...)

files that are specific to that deployment are created in the deploy dir
"""

import os
import os.path

#dir tree:

#- /my_django_root/apps/
#- /              /projects/project_root/apps/
#- /              /                     /templates/
#- /              /                     /project_root/settings.py
#- /              /static/
#- /              /templates/

project_root    = os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) )
my_django_root  = os.path.dirname( os.path.dirname( project_root ) )

#for current project only:
project_apps_dir            = os.path.join( project_root, 'apps' )
project_templates_dir       = os.path.join( project_root, 'templates' )
project_static_files_dir    = os.path.join( project_root, 'static' )

#may be shared between projects:
global_apps_dir         = os.path.join( my_django_root, "apps" )
global_templates_dir    = os.path.join( my_django_root, "templates" )
global_static_files_dir = os.path.join( my_django_root, "static" )

DATABASES = {
    'default': {
        'ENGINE'    : 'django.db.backends.mysql',   # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME'      : 'elearn_django',              # Or path to database file if using sqlite3.
        'USER'      : 'test',                       # Not used with sqlite3.
        'PASSWORD'  : 'asdf',                       # Not used with sqlite3.
        'HOST'      : '',                           # Set to empty string for localhost. Not used with sqlite3.
        'PORT'      : '',                           # Set to empty string for default. Not used with sqlite3.
    }
}
