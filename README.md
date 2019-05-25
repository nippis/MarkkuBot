# MarkkuBot

MarkkuBot tai kutsumanimeltään Markku on TT-Kameroiden telegram-chattia varten tehty botti jonka päätehtävä on kertoa onko kerhohuoneella valot päällä. Markulle on ajan mittaan opetettu muitakin temppuja kuten kiittämisen jalo taito.

## Docker

Markun toteutus on siirretty Dockerissa pyöriväksi. Vaikka Markkua pystyy edelleen ajamaan ilman Dockerin apua, se helpottaa huomattavasti toimintaa. Kehittämiseen ja julkaisuun tarvitaan siis Dockeria ja Docker-composea.

### Kehitys

Kehitys onnistuu helpoiten komennolla `docker-compose up --build` tai `docker-compose up --build -d` jos haluat ajaa detached-tilassa. 

### Tuotanto

*Tähän saadaan toivottavasti automatisointi jatkossa.*

Markun image rakennetaan komennolla `docker build -t markkubot:x.x.x .`, missä x.x.x on uusi versionumero. Tarkista nykyinen komennolla `docker ps`. Tämä numero pitää kirjoittaa myös docker-compose.yml tiedostoon.

Tuotantokoneella Markkua kannattaa ajaa stackina eli komennolla
`docker stack deploy -c docker-compose.yml --resolve-image never markku`,
missä `-c` kertoo docker-compose -filun polun, `--resolve-image never` ei tarkista ajettavia imageja Docker Hubista (jos imaget lokaalisti buildattuja) ja viimeinen parametri asettaa stackille nimen, tässä tapauksessa "markku". Stackin päivittäminen tapahtuu samalla komennolla.

Ylläoleva komento on kirjoitettu valmiiksi update.sh tiedostoon. 

### .env

env-tiedostossa Markulle tärkeät jutut (keksi sopivat nimet itse, esim. `markku_chats_collection` jne.):

```
TG_TOKEN=<telegramin bot token>
DB_NAME=<tietokannan nimi>
CHATS_COLL_NAME=<tietokannan chat-collectionin nimi>
WORDS_COLL_NAME=<tietokannan sana-collectionin nimi>
BLACKLIST_COLL_NAME=<tietokannan blacklist-collectionin nimi>
SENSOR_API_ADDRESS=<pimiödatan api:n osoite>
```

## Huomattavaa

Muista uuden botin privacy mode pois.

HUOM: Samasta koodiversiosta myös tägi githubiin samalla versionumerolla, `git tag -a x.x.x -m "x.x.x" && git push --tags`, `-a` tekee annotoidun tagin (joka on ihan hyvä olla) ja tällöin sille joutuu heittämään jonkun viestin.

## ROADMAP

* PostgreSQL
* Githubista automatisoidut Docker-buildit: https://docs.docker.com/docker-hub/github/#github-organizations
* Tuotantoon joku haistelija, joka hakee uusimman buildin Docker Hubista ja käynnistää Markun uudelleen

