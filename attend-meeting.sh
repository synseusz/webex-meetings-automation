#!/bin/bash

#Activate webex venv
source ./webex-env/bin/activate

#Check for meeting host
if [ "$1" ]; then
  echo "Meeting with -" $1
  ./python/meeting.py $1
else
  echo "No meeting host argument provided while executing script.."
  echo "Please provide who is a meeting host (W3 EMAIL):"
  read HOST
  echo $HOST
  ./python/meeting.py $HOST
fi

exit
