#!/usr/bin/env pandoc

#index

#genearal sources
  
  http://www.djangobook.com
  http://djangosnippets.org/

#db interaction

  https://docs.djangoproject.com/en/dev/ref/models/fields/
  https://docs.djangoproject.com/en/dev/ref/models/relations/
  https://docs.djangoproject.com/en/dev/topics/db/queries/
  #learn _set + related_name magic

#template language

  https://docs.djangoproject.com/en/dev/topics/templates/
  https://docs.djangoproject.com/en/dev/ref/templates/builtins/
  
  date:
    https://docs.djangoproject.com/en/dev/ref/templates/builtins/?from=olddocs
    https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date-time

  two fields that are unique together
    http://blog.gordaen.com/2009/07/08/mysql-unique-key-pairs/

  context processor: define variables for every single template
    https://docs.djangoproject.com/en/dev/ref/templates/api/#writing-your-own-context-processors
    http://blog.madpython.com/2010/04/07/django-context-processors-best-practice/
    http://www.b-list.org/weblog/2006/jun/14/django-tips-template-context-processors/

#forms

  https://docs.djangoproject.com/en/dev/topics/forms/
  https://docs.djangoproject.com/en/dev/ref/forms/fields/
  https://docs.djangoproject.com/en/dev/ref/forms/api/
  https://docs.djangoproject.com/en/dev/ref/forms/widgets/
  http://tothinkornottothink.com/post/10815277049/django-forms-i-custom-fields-and-widgets-in-detail
    custom widgets
  https://docs.djangoproject.com/en/dev/ref/forms/validation/

  http://mikepk.com/2010/08/python-django-forms-errors-fieldsets/
  #form customization. confirm email field.

  http://charlesleifer.com/blog/djangos-inlineformsetfactory-and-you/
  #poll choices create at same time form

  http://jayapal-d.blogspot.com.br/2009/08/reuse-django-admin-filteredselectmultip.html#comment-form
  #how to reuse django admin filteredselectmultiple

#static content
  

#pagination: 

  https://docs.djangoproject.com/en/dev/topics/pagination/?from=olddocs

#user login

  request context to use user in template. render vs render_to_response
     https://docs.djangoproject.com/en/dev/topics/http/shortcuts/#django.shortcuts.render


#good apps

#required for mysql:

    #high level table operations:

        sudo pip install django_tables2

    #easy user creation/login:

        sudo pip install django-userena

#TODO

 serve project specific static files in app urls

 define commands outside apps
 count foreign key inverse
 get field names/verbose names in templates
 generic views for inlineformset
   https://github.com/AndrewIngram/django-extra-views
   https://docs.djangoproject.com/en/1.4/topics/forms/modelforms/#inline-formsets
 generic views that depend on request:
   user / list something that belongs to the user
 enforce unique username/groupname User/group

#get started

##install

``` {.bash}
sudo aptitude install -y python-mysqldb
sudo pip install django
```

``` {.bash}
python -c "import django; print(django.get_version())"
```

##create project

#create template dir structure some files:

``` {.bash}
p=
django-admin.py startproject $p
    #create a new project called p
```

##create database

    #setup database connexions
    cd $p
    vim settings.py
        #ENGINE: 'django.db.backends.postgresql_psycopg2', 'django.db.backends.mysql', 'django.db.backends.sqlite3' or 'django.db.backends.oracle
        #NAME: db name. for sqlite, it is a file, so give full path. for mysql, it is just the name
        #USER: user you set up with the db
        #PASS: pass you set up with the db
        #HOST: empty if local machine

    mysql -u '<USER_NAME>' -p
    create database <DB_NAME>
    #create the database

##run test server

    for this to work:

    python manage.py runserver
        #startd dev server on default port

##visit website

    firefox http://127.0.0.1:8000/ 

#apps

    #apps are nothing but regular python modules

    #therefore, all you need to do to create one is put the app dir in your PYTHONPATH,
    #and add a __init__.py in the app dir so that it is seen as a python app.

    #i am not sure if the default file names such as models.py, urls.py, etc.
    #are magic/required, but if if not you should keep and use them for uniformisation's sake

    #create

        #create tamplate directories/files for an application:
            python manage.py startapp $APP_NAME

            #TEMPLATE_LOADERS = (
                #'django.template.loaders.app_directories.Loader',
            #)
        #templates in that dir will be loaded under $APP_NAME/$TEMPLATE_NAME
        #when the when in settings.py you have:
            cd $APP_NAME
            mkdir "templates/$APP_NAME"

        #templates

            #to make templates as pluggable as possible, use the following conventions:

            {% extends "mnemosyne/base.html" %}
            #all the app templates extend a single base app template

            #use the following fields for your sites base.html template
            #and in the apps use those fields, extend the base template from the apps base templat/
                #title : inside head, must be <title>-safe, so no formatting
                #extrahead : extra stuff to add to head
                #content_title : title of the content, inside body, no <hX> tag just text imho,
                    #so that base page can define a all in a single way
                #content; the main content of the document 

    #install external app

        sudo pip install django_usereana

    #enable

        #/INSTALLED_APPS, add $APP_NAME to the list
            vim $PROJECT/settings.py

        #shows a dry run of the necessary sql statements to make the APP_NAME app:
            ./manage.py sql $APP_NAME

        #update database to add the models which are in active apps:
            ./manage.py syncdb
        #the list of activated apps can be found in PROJ/settings.py > INSTALLED_APPS

    #remove

        ./manage.py sqlclear my_app_name
        #remove app from db

        vim $PROJECT/settings.py
        #/INSTALLED_APPS, remove from list

    #app commands
        https://docs.djangoproject.com/en/dev/howto/custom-management-commands/

        cd $APP_ROOT
        mkdir management/commands
        cd management
        touch __init__.py
        cd commands
        touch __init__.py
        vim command.py

##test

    ./manage.py test     #test all apps
    ./manage.py test app #test given apps

##database

    #<https://docs.djangoproject.com/en/dev/topics/db/queries/>

    ./manage.py shell
        #interactive python shell with special path variables set
        #can be used to:
        #  modify db

    #create:

        p = Obj()
        p.save()
        #create object and save it to db

        p = Obj.objects.create()
        #same as above

    #get 

        #gets all objects
        for o in Obj.objects.all():
            print o

        #filter by fields
        for o in Obj.objects.filter(pub_date__year=1):
            print o

        #exclude by fields
        for o in Obj.objects.exclude(pub_date__year=1):
            print

        #chain filters
            Entry.objects.filter(
                headline__startswith='What'
            ).exclude(
                pub_date__gte=datetime.date.today()
            ).filter(
                pub_date__gte=datetime(2005, 1, 30)
            )

    #delete

        o.delete()

    #foreign key
        #on delete of referenced object, deletes pointer too!

#static

it is very slow to serve static files through wsgi or cgi

you must let the server to that for you

in settingsset ``STATIC_ROOT`` to somwhere where the server sees the static files:

    STATIC_ROOT = "/var/www/root/django/projectname/static"

this would be a good setting, supposing you have serve root at ``/var/www/root/``.

dev server takes root at the root of the project

to automatically copy all static files to ``STATIC_ROOT`` do:

``` {.bash}
    ./manage.py collectstatic
```

any missing dirs are created.

remember that you must have the permission to copy those files there.
which normal users usually don't by default

finally, give the preffix to all static files with static url:

    STATIC_URL = 'http://localhost/django/elearn/static'

note how the http://localhost/ part could be anything,
but the ``/django/elearn/static`` must be exactly that
unless you use aliases.

#pagination

#templates

    ### custom_templates.py ###

    from django import template
    register = template.Library()

    @register.simple_tag

    def custom_tag_field(value, kwarg1=False, kwarg2=False):
        t = template.loader.get_template('some_template.html')
        return t.render(template.Context({'value': value, 'kwarg1':kwarg1, 'kwarg2': kwarg2}))

    ### index.html ###

    {% load custom_templates  %}
    {% get_with_args_and_kwargs somevar,"sometext",kwarg1=someothervar %}

#commands

    #open mysql, password from settings file:

        ./manage.py dbshell

    ./manage.py sqlclear accounts | ./manage.py dbshell

#forms

    #cusomize form input attributes
    from django import forms
    class F(forms.Form)
        city = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'autocomplete':'off',
                    'form':form,
                }
            )
        )

##debugging
    
    #run server in a mode where warnings give errors:

        python -W error manage.py runserver

    #this way you can view a traceback for the error and spot its origin

##south

    #info

        #http://south.readthedocs.org/en/latest/tutorial/part3.html

        #there are two parts to south:
            #south db: stores when migration were applied
            #migration files: say what migrations whould do

        #schema migrations
            #layout of columns
            #renaming, creating

    #install south:

        sudo pip install south

    #installation on project:

        #add to INSTALLED_APPS
        ./manage.py syncdb

    #add a table to tracking *before* a syncdb:
        
        ./manage.py schemamigration --initial "$APP"
        #creates migration files

        ./manage.py migrate "$APP"
        #applies migration, changing south db and creating app db
            #only migration file is considered for this:
            #if you change your model after the shcemamigration,
            #migrating directly will do nothing! you must do another
            #schemamigration

            #./manage.py syncdb does nothing to an app that is tracked by south

    ##migrate

        ./manage.py migrate --list
        #see a list of available migrations
            #simply lists files in migration folders
            #* means applied

        #travel in time
            ./manage.py migrate #go to latest migration
            ./manage.py migrate "$APP" 0002
            #go back to migration 2
                #called *rollback*

            ./manage.py migrate "$APP" zero
            #initial state, removes from south db

    #add a table to tracking *after* syncdb
        ./manage.py convert_to_south "$APP"
        #convert existing table to south:
            #makes migration file
            #applies migration on south db
            #table data is untouched

    #simple migrations: auto can recognize changes
        #add new field to tracked table

        ./manage.py schemamigration "$APP" --auto
        #new fields must have default
        ./manage.py migrate

    #more complex migrations
        ./manage.py datamigration "$APP" "$NAME"

        #you must edit the migration files yourself
   
        #change field attributes

        #rename model field

            ### generated file ###
            from .. import settings.THISAPP as app

            class Migration(DataMigration):

                def __init__(self):
                    self.table = app + '_' + ''
                    #learn how django calculates table names
                        #app + '_' + class.lower()
                        #_id is appended if foreign key
                        #always have a peek at db before migration
                    self.old = ''
                    self.new = ''
                    #self.unique_with = ['',] #unique together, except for changing key

                def forwards(self, orm):
                    db.rename_column(self.table, self.old, self.new)
                    #db.create_unique(self.table, unique_with + self.new)

                def backwards(self, orm):
                    db.rename_column(self.table, self.new, self.old)
                    #db.create_unique(self.table, unique_with + self.old)

        #rename model
            #http://stackoverflow.com/questions/2862979/easiest-way-to-rename-a-model-using-django-south

            ### generated file ###
            from .. import settings.THISAPP as app

            class Migration(SchemaMigration):

                def __init__():
                    self.old_model = ''
                    self.new_model = ''
                    self.old_db = self.model_to_db(self.old_model)
                    self.new_db = self.model_to_db(self.new_model)

                def model_to_db(self,model):
                    return app + '_' + model.lower().strip('_')

                def forwards(self, orm):
                    db.rename_table(self.old, self.new) 
                    #deal with foreign keys
                    db.send_create_signal(app, [self.new_model])

                def backwards(self, orm):
                    db.rename_table(self.new, self.old)
                    #deal with foreign keys
                    db.send_create_signal(app, [self.old_model])

#apache deploy

this is a checklist for deployment with ``Apache``

- make sure that the apache user ( ``www-data`` by default on ubuntu ) has read permissions to all files below!

    for this, it needs to have read premissions to all the directories above those files too.

- point ``mod_wsgi`` to use your ``wsgi.py`` script, located by default in ``appname_wsgi/wsgi.py``

    the actual location of that script has no importance

- ensure that the following are in the ``mod_wsgi`` pythonpath:

    - ``settigs.py``

    - ``urls.py``

    - all your apps

    append to this path with the ``WSGIPythonPath`` directive.

- ensure that static files are being served where your app expects them to be

    Consider using the ``Alias`` directive from ``SATIC_URL`` to ``STATIC_DIR``

- ensure that ``TEMPLATE_DIR`` contains the correct path to your cross project templates.
