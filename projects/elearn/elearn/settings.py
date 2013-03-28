# Django settings for elearn project.

import os
import os.path
import sys

from django.core.urlresolvers import reverse

import django.conf.global_settings as DEFAULT_SETTINGS

#===================================================
# dir tree
#===================================================

#dir tree:
#- /my_django_root/apps/
#- /              /projects/project_root/apps/
#- /              /                     /templates/
#- /              /                     /project_root/settings.py
#- /              /static/
#- /              /templates/

#app load order is given by the python path
#template load order will be:
#  system template dirs
#  app template dirs

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
my_django_root = os.path.dirname(os.path.dirname(project_root))

#for current project only:
project_apps_dir = os.path.join(project_root,'apps')
project_templates_dir = os.path.join(project_root,'templates')
project_static_files_dir = os.path.join(project_root,'static')

#ma be shared between projects:
global_apps_dir = os.path.join(my_django_root,"apps")
global_templates_dir = os.path.join(my_django_root,'templates')
global_static_files_dir = os.path.join(my_django_root,'static')

sys.path.append(project_apps_dir)
sys.path.append(global_apps_dir)

#===================================================
# non app settings
#===================================================

INSTALLED_APPS = [

    #standard:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles', #to find static files
    'django.contrib.admin',
    #'django.contrib.admindocs',

    #pypi:
    'guardian',
    'easy_thumbnails',
    'south',

    #personal:
    'polls',
    'mycommands',
    'user_user_groups',
    'user_list_uri',
    'issue_tracker',
    'project_specific',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'elearn_django',              # Or path to database file if using sqlite3.
        'USER': 'test',                       # Not used with sqlite3.
        'PASSWORD': 'asdf',                   # Not used with sqlite3.
        'HOST': '',                           # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                           # Set to empty string for default. Not used with sqlite3.
    }
}

#which urls.py file to use for entire site:

ROOT_URLCONF = 'elearn.urls'

#it must be in the pythonpath.

#<https://docs.djangoproject.com/en/dev/ref/settings/#append-slash>
APPEND_SLASH=True

#Python dotted path to the WSGI application used by Django's runserver:
WSGI_APPLICATION = 'elearn.wsgi.application'
#must be in pythonpath

# Make this unique, and don't share it with anybody.
SECRET_KEY = '59wh9zzfvdj09owpp0=+w=nc_nmdw_*(k*0yw=uq_2k7au2or4'

SITE_ID = 1

##media

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

##debug

#users listed unser ADMINS will get emails whenever an uncaught exception
#happens and if DEBUG is True
#Those exceptions are always logged into the server's error logs.
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

##static

#static files are stuff like css and images
#for deployement, set STATIC_ROOT and do : ./manage.py collectstatic
#this will put all the static files collected (including from apps)
#into the that static root
STATIC_ROOT = '/var/www/root/django/elearn/static'

#prefix to be used for static files.
#will be exported to template files by some module included by default.
#you must set your web server to serve files from STATIC_ROOT at that url location
STATIC_URL = 'http://localhost/django/elearn/static/'

#in this example, supposing apache has serve root at /var/www/root, it will work

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    project_static_files_dir,
    global_static_files_dir,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

##template

#context processors: add context to every template

#TEMPLATE_CONTEXT_PROCESSORS.append('django_tables2_datatables.context_processor.processor')

#must be absolute paths
# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (
    project_templates_dir,
    global_templates_dir,
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (

    'django.template.loaders.filesystem.Loader',
    #loads files specified in TEMPLATE_DIRS

    'django.template.loaders.app_directories.Loader',
    #looks for templates inside the "templates" app dirs

#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = list(DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS)

##timezone

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

##datetime

#default date format. l10n has precedence over this if l10n is true.

DATE_FORMAT="Y-m-d"
DATETIME_FORMAT = "Y-m-d H:i:s"
SHORT_DATETIME_FORMAT = "Y-m-d H:i:s"

#===================================================
# apps
#===================================================

## userena

#add apps required by userena
INSTALLED_APPS.extend([
    'userena',
    'accounts',
])

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

### email settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
#EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 25
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mytemanu0@gmail.com' #confirmation mails will be sent from this email. not all hosts work, gmail does.
EMAIL_HOST_PASSWORD = 'thpaofmyte'

ANONYMOUS_USER_ID = -1

#LOGIN_REDIRECT_URL = '/users/%(username)s/'
USERENA_SIGNIN_REDIRECT_URL = '/users/%(username)s/'
LOGIN_URL = '/users/signin/'
LOGOUT_URL = '/users/signout/'

#see userena.settings for the stuff you can change!
AUTH_PROFILE_MODULE = 'accounts.Profile' #what module to user for profile. extends UserenaBaseProfile
USERENA_PROFILE_LIST_TEMPLATE = 'accounts/profile_list.html'
USERENA_PROFILE_DETAIL_TEMPLATE = 'accounts/profile_detail.html'
#USERENA_HIDE_EMAIL=True

##datatable

INSTALLED_APPS.extend([
    'django_tables2',
    'django_tables2_datatables',
    'master_checkbox',
])
