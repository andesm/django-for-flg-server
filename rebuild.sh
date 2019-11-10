#!/bin/bash -x
git add . && git commit -m "Organize the configuration" && git push
oc login -u andesm -p a
oc start-build django-for-flg-server
