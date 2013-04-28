"""
contains settings that change with different deployments

this version is for openshift deployment.

this is done so as to allow simple deployment only using symlinks

files that stay the same with deployments are symliked to a deploy dir (git, ftp...)

files that are specific to that deployment are created in the deploy dir
"""

import os
import os.path

#dir tree:
#- django_root/
#-            /my_django_root/
#-            /              /lib/elearn/
#-            /              /          /settings.py
#-            /              /          /urls.py
#-            /              /apps/
#-            /              /templates/
#-            /              /static/
#-            /              /projects/project_root/apps/
#-            /              /                     /templates/
#-            /              /                     /static/
#-            /deploy/openshift/openshift_project_name/wsgi/static

#template load order will be:
#  system template dirs
#  app template dirs

my_django_root  = os.path.dirname( os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ) )

project_root    = os.path.join( my_django_root, 'projects', 'elearn' )

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
        'ENGINE'    : 'django.db.backends.mysql',
        'NAME'      : 'test',
        'USER'      : os.environ['OPENSHIFT_MYSQL_DB_USERNAME'],
        'PASSWORD'  : os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'],
        'HOST'      : os.environ['OPENSHIFT_MYSQL_DB_HOST'],
        'PORT'      : os.environ['OPENSHIFT_MYSQL_DB_PORT'],
    }
}

STATIC_ROOT = os.path.join( os.path.dirname( my_django_root ), 'deploy', 'openshift', openshift_project_name, 'wsgi', 'static' )
STATIC_URL = 'http://' + openshift_project_name + 'djangoelearn-cirosantilli.rhcloud.com/TODO'
