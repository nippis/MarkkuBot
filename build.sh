#!/bin/bash
# stty icanon

current=$(docker ps | grep markkubot: | awk {'print $2'})
echo "Nykyinen nimi + tägi on '$current', mikä tägi uuteen versioon tulee?"
read -p "markkubot:" newtag
echo
newname="markkubot:$newtag"
echo "Rakennetaan $newname..."
docker build -t $newname .
