#!/usr/bin/env bash

#find files that I want to keep track of for a django project,
#and adds them to django

set -e #stop execution if one command goes wrong

ack-grep --ignore-dir=migrations -ag '\.(py|html|css|js|md|jpg|jpeg|png|ico|gif)$' | xargs -I'{}' git add '{}'

exit 0
