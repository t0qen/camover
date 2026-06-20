#!/bin/bash

echo "CAMOVER DEVELOPPEMENT INIT"
echo "--"
read -p "battery plugged ?"
read -p "power switch ok ?"

echo

echo "1) start the robot"
echo
echo "(waiting 2s for xiao turns on)"

for i in {1..10}; do
    printf "#"
    sleep 0.2
done
echo
echo
echo "- test xiao conection"
if ping -c 1 192.168.1.11 >/dev/null 2>&1; then
    echo "xiao ok"
else
    echo "* xiao problem *"
    exit
fi

echo
echo "- switch relay thought home assistant"
http_code=$(curl -s -o /dev/null -w "%{http_code}" -X POST   -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhN2E4ZmM5Y2E4NDQ0M2I5YTg1MzFiMzhkOTk1NGU5OCIsImlhdCI6MTc4MTk3NTU3MSwiZXhwIjoyMDk3MzM1NTcxfQ.hYHe9X5drH7PH0W4smQ3SaFfJ-6OYVScBuh14ey5Jxo" -H "Content-Type: application/json" -d '{"entity_id":"switch.camover_s_pi"}' "http://192.168.1.23:8123/api/services/switch/turn_on")

if [ "$http_code" = "200" ]; then
    echo "request ok"
else
    echo "* home assitant problem *"
    exit
fi
echo 
echo
echo "(waiting 60s for pi booting)"
for i in {1..10}; do
    printf "#"
    sleep 6
done
echo
echo
echo "- test pi connection"

if ping -c 1 192.168.1.37 >/dev/null 2>&1; then
    echo "pi ok"
else
    echo "* pi problem *"
    exit
fi
echo 

echo "2) setup developpement environnement"
echo
echo "- mount pi storage to pc"
sshfs pi@192.168.1.37:/home/pi/camover /media/aymeric/PROJECTS/camover/src &
echo
echo "- open folder in vscode"
code /media/aymeric/PROJECTS/camover &
echo
ssh pi@192.168.1.37 &


































