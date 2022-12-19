#!/bin/bash

# on startup crontabs -e changes path to /home/my-username and starts startup.sh
# startup.sh does the following: 

# 1. It changes the path to Code/Python/Projects/Caines 
# 2. starts the virtualenv
# 3. runs cronjob.sh that runs main.py
# 4. deactivates virtualenv

cd Code/Python/Caines-Email/caines

source ../env/bin/activate

date="DATE: "$(/bin/date +%H:%M/%d-%m-%y)
script=$(./main.py 2> error.txt)
retval=$?

if [ "$retval" -eq 0 ]; then
        echo "$date OUTPUT: $script" >> log.txt
else
        echo "$date OUTPUT: FAIL PLEASE LOOK AT ERROR.txt" >> log.txt
fi

deactivate
