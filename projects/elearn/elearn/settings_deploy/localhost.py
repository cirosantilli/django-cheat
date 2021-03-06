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

#- my_django_root/apps/
#-               /projects/project_root/apps/
#-               /                     /templates/
#-               /                     /project_root/settings.py
#-               /static/
#-               /templates/

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

#one common server strategy is to give sensitive values such as passwords
#is to give them as environment variables.
#so you can just add it to a public git repo directly
DATABASES = {
    'default': {
        'ENGINE'    : 'django.db.backends.mysql',   # 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME'      : 'elearn_django',              # path to database file if using sqlite3, db_name otherwise.
        'USER'      : 'test',                       # not used with sqlite3.
        'PASSWORD'  : 'asdf',                       # not used with sqlite3.
        'HOST'      : '',                           # set to empty string for localhost. Not used with sqlite3.
        'PORT'      : '',                           # set to empty string for default. Not used with sqlite3.
    }
}

#static files are stuff like css and images
#for deployement, set STATIC_ROOT and do : ./manage.py collectstatic
#this will put all the static files collected (including from apps)
#into the that static root
STATIC_ROOT = '/var/www/root/django/elearn/static'

#prefix to be used for static files.
#will be exported to template files by some module included by default.
#you must set your web server to serve files from STATIC_ROOT at that url location
STATIC_URL = 'http://localhost/django/elearn/static/'
