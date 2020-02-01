#!/bin/bash -x

time oc exec $(oc get pods | grep 'django-for-flg-server.*Running' | awk '{print $1}') ./diary.sh
