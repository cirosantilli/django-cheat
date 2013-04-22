#!/usr/bin/env bash
set -u # error on undefined variable
set -e # stop execution if one command return != 0

#this script automates my django deployment

#this is just a prototype before I do it in python and use info from settings.py

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

        #same as djangos STATIC_ROOT conf: (TODO get this using python...)

            static_root="/var/www/root/django/elearn/static"

    ##main

        project_dir=projects/"$project_name"/
        settings_dir="$project_dir$project_name"/
        clone_libs_dir="${clone_dir}libs/"
        clone_settings_dir="$clone_libs_dir$project_name/"
        clone_wsgi_dir="${clone_dir}wsgi/"
        clone_static_dir="${clone_wsgi_dir}static/"

        cp -lru "$static_root"*                 "$clone_static_dir"
        cp -lru "$modules_dir"*                 "$clone_libs_dir"

        cp -lru *                                                   "$clone_dir"
        mv      "$clone_dir$settings_dir"       "$clone_settings_dir"
        cd      "$clone_settings_dir"
        rm      settings.py
        ln -s   settings_deploy/openshift.py    settings.py
        mv      wsgi.py                         "${clone_wsgi_dir}application.py"
        cd  "$clone_dir"
        git add *
        git commit -am 'upload'
        git push origin master

fi
