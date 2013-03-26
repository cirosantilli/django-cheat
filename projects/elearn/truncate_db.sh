#!/usr/bin/env bash

#removes all entries from all tables on project

./manage.py issue_tracker__truncate_db
./manage.py user_list_uri__truncate_db
./manage.py user_user_groups__truncate_db
./manage.py accounts__truncate_db
