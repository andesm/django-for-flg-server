#!/bin/bash -x

oc login -u andesm -p a
time oc exec $(oc get pods | grep 'django-for-flg-server.*Running' | awk '{print $1}') ./diary.sh
