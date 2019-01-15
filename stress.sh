#! /bin/bash
# Timeout for stress test
hr=0
min=0
sec=3
duration=hr*3600+min*60+sec
upload=0
download=0
clean=0

# python token.py Start token.conf &
# sleep 25

python connect.py Start connect.conf &
sleep 180

if [ $upload -gt 0 ]
then
    endTime=$(( SECONDS+$duration ))
    while [ $SECONDS -lt $endTime ]
    do
        python upload.py Start upload.conf
        sleep 1
    done
fi
if [ $download -gt 0 ]
then
    endTime2=$(( SECONDS+$duration ))
    while [ $SECONDS -lt $endTime2 ]
    do
        python download.py Start download.conf
        sleep 1
    done
fi
python connect.py Stop connect.conf
sleep 5
if [ $clean -gt 0 ]
then
    python delete.py Start delete.conf
    sleep 3
    python trash.py Start trash.conf
    sleep 3
fi

# python token.py Stop token.conf
# sleep 3
