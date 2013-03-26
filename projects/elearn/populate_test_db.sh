#!/usr/bin/env bash

#inserts test entries into database

./manage.py accounts__populate_test_db
./manage.py user_user_groups__populate_test_db
./manage.py user_list_uri__populate_test_db
./manage.py issue_tracker__populate_test_db
