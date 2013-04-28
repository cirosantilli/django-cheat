#!/usr/bin/env bash

set -u # error on undefined variable
set -e # stop execution if one command return != 0

#this script automates my django deployment

#this is just a prototype before I do it in python and use info from settings.py

#the main ideas are:

#- separated deployment specific settings from other settings (dbs, etc) and symlink to the right one

#- hardlink everything to the deploy dir. It is quick and memory cheap to create hardlinks.

#suggested dir structure:

#- django/
#-       /deploy/openshift/djangoelearn/                            clone_dir
#-       /      /         /            /libs                        clone_libs_dir
#-       /      /         /            /wsgi                        
#-       /devpath/
#-       /userid/
#-       /      /THIS_SCRIPT
#-       /      /projects
#-       /      /        /project_name                              project_dir
#-       /      /        /            /project_name/                settings_dir
#-       /      /        /            /            /wsgi.py
#-       /      /        /            /            /settings.py
#-       /      /apps
#-       /      /static
#-       /      /templates

##openshift deployment

if true; then

    ##inputs

        #absolute path to where you cloned from openshift

        #ex: 

            #cd /var/www/django/deploy/openshift/
            #git clone ssh://514c77f2e0b8cd7551000165@test-cirosantilli.rhcloud.com/~/git/test.git/ test

            clone_dir="../deploy/openshift/djangoelearn/"

        #a dir that contains (symlinks) to all your python modules that are not available in pypi

        #for example modules that you forked

            #example:

                #ln -ds /path/to/my/forked/module1 "$modules_dir"/module1
                #ln -ds /path/to/my/forked/module2 "$modules_dir"/module2

            modules_dir="../devpath/"

        #name of the dir under projects:

            project_name="elearn"

        #name of the app at openshift:

            openshift_project_name="elearndjango"

        #same as djangos STATIC_ROOT conf: (TODO get this using python...)

            static_root="/var/www/root/django/elearn/static/"

    ##main

        project_dir=projects/"$project_name"/
        settings_dir="$project_dir$project_name"/
        clone_libs_dir="${clone_dir}libs/"
        clone_settings_dir="$clone_libs_dir$project_name/"
        clone_wsgi_dir="${clone_dir}wsgi/"
        clone_static_dir="${clone_wsgi_dir}static/"

        cp -lr      "$static_root"*                 "$clone_static_dir"
        cp -Llr     "$modules_dir"*                 "$clone_libs_dir"
        cp -lrf     * .gitignore                    "$clone_dir"

        mv          "$clone_dir$settings_dir"       "$clone_settings_dir"
        cd          "$clone_settings_dir"
        mv          settings_deploy/openshift.py    settings_deploy.py
        rm -r       settings_deploy/
        mv          wsgi.py                         ../../wsgi/application
        cd -

        #commit
        cd  "$clone_dir"
        git add *
        git commit -am 'upload'
        git push -f origin master

        #clean up deploy repo:
        git reset --hard HEAD~
        git clean -df

        rhc app restart -a "$openshift_project_name"
fi
