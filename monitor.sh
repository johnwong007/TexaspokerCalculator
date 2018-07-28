#!/bin/bash

CheckProcess()
{
    procCount=`ps -af |grep "manage.py" |grep -v "grep" |wc -l`
    if [ "$procCount" -eq "0" ];
    then
        echo 'ps' "manage.py" 'return 0'
        return 0
    else
        echo 'ps' "manage.py" 'return 1'
        return 1
    fi
}

while ((1))
do
    nowtime=`date +%H%M%S`
    echo '********** will check, currtime:' ${nowtime}
    CheckProcess "GATE"
    retCP=$?
    if [ $retCP -eq "0" ]
    then
        echo '**************** will start server.....'
        exec python manage.py runserver 0.0.0.0:80 &
    fi

    sleep 20
done

