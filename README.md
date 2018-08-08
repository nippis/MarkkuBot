# MarkkuBot

TT-kameroiden virtuaalinen maskotti.

## Docker

Markun toteutus on siirretty Dockerissa pyöriväksi. Vaikka Markkua pystyy edelleen ajamaan ilman Dockerin apua, se helpottaa huomattavasti toimintaa. Kehittämiseen ja julkaisuun tarvitsee siis Dockerin sekä Docker Hub -tunnarit.

### Kehitys

Kehitystä tehdessä helpointa on pitää MongoDB lokaalissa Dockerissa ajossa, ja buildata ja käynnistää Markku aina testattaessa.

Mongon saa ajoon `docker run -d mongo:3.6.6`, jossa `-d` ajaa konttia detached modessa, eli kontti pysähtyy jos ajava prosessi pysähtyy (https://docs.docker.com/engine/reference/run/#detached--d). Kontin voi myös käynnistää lisäparametrillä `--rm`, joka poistaa kontin sisällön (mukaanlukien tietokannan) poistuttaessa.

Markun Docker-image kasataan komentamalla `docker build -t markkubot:x.x.x .`, jossa `-t` antaa imagelle tägin, tässä tapauksessa markkubot, versio x.x.x. Lopun `.` on polku kansioon, josta löytyy Markun Dockerfile.

Markun saa ajoon komennolla `docker run -it --link=joku_kontti:mongo --rm --env-file=.env markkubot:0.0.1`. `-it` käynnistää kontin interaktiivisessa tilassa, eli logit näkyy. `--link` yhdistää Mongo-kontin Markku-konttiin, eli sille parametrina kontin_nimi:mongo (nimi selviää ajamalla `docker ps`, esim. "eloquent_shtern"). `--env-file` antaa Markku-kontille tarvittavat ympäristömuuttujat, mukaanlukien Mongon IP:n ja portin.

Kehittäessä voi myös ajaa Markkua docker composen avulla, mutta se muuttaa tiettyjä juttuja. Testaus käytännössä Tuotantojulkaisun mukaisesti, mutta deploylle:lle annetaan `docker-compose-dev.yml` joka lisää stackiin mongo-express -web-UI:n MongoDB datan tutkailuun. **MONGO-EXPRESS EI SAA MENNÄ TUOTANTOON.** Mongo-expressin käli löytyy osoitteesta http://localhost:8081

### 🚧 WIP 🚧 Tuotanto

Buildataan image, tägätään image jotta se saadaan yhdistettyä Docker Hub:n repoon, pushataan image.

```
docker build -t markkubot:x.x.x .
docker tag markkubot:x.x.x <docker username>/markkubot:x.x.x
docker push <docker username>/markkubot:x.x.x
```

HUOM: Samasta koodiversiosta myös tägi githubiin samalla versionumerolla, `git tag -a x.x.x -m "x.x.x" && git push --tags`, `-a` tekee annotoidun tagin (joka on ihan hyvä olla) ja tällöin sille joutuu heittämään jonkun viestin.

Tuotantokoneelle MarkkuBot-repon `docker-compose.yml` ja `docker stack deploy -c docker-compose-dev.yml markku`

### .env

env-tiedostossa Markulle tärkeät jutut:

```
TG_TOKEN=<telegramin bot token>
DB_NAME=<tietokannan nimi>
CHATS_COLL_NAME=<tietokannan chat-collectionin nimi>
WORDS_COLL_NAME=<tietokannan sana-collectionin nimi>
```

## Huomattavaa

Muista uuden botin privacy mode pois. Moden päivityksen jälkeen botti pitää potkia ja lisätä uudestaan

## ROADMAP

* Mongon tieturvallisuutta voi parantaa käyttäjätunnareilla melko helposti
* Githubista automatisoidut Docker-buildit: https://docs.docker.com/docker-hub/github/#github-organizations
* Tuotantoon joku haistelija, joka hakee uusimman buildin Docker Hubista ja käynnistää Markun uudelleen

## ⚠️ Deprecated ⚠️ Vanha Markku ja MongoDB

Periaatteessa Markkua voisi edelleen ajaa vanhaan tapaan, mutta ei kannata. Settings.json on korvattu env-tiedostolla

### Uuden MongoDB:n pystytys

* Asenna MongoDB 4.0.0 (stable): https://docs.mongodb.com/manual/installation/#tutorials
* Varmista, että voit ajaa `mongod` komennon termiksestä.
* Asenna python-riippuvuudet. Kehitysympäristössä voi olla fiksua luoda virtuaaliympäristö esim. `virtualenv`-komennolla riippuvuuksia varten.
* Käynnistä Mongo-serveri `mongod`-komennolla. Serverille voi määrittää tietokannan sijainnin, defaulttina `/data/db` mutta db:n voi laittaa vaikka projektikansioon:
```
mongod --dbpath <projektikansion polku>/db
```
* Laita Markku päälle. Markku yhdistää Mongoon Mongon default-portin `localhost:27017` kautta.
* Mongon tietokannan ja collectionin nimet haetaan `settings.json`:ista.
* Tietokantaa voi tökkiä termiksestä ajamalla `mongo`. Komento yhdistää default-asetuksilla pystytettyyn kantaan ja avaa Mongon oman konsolin termiksen sisälle.

### Yleistä infoa Mongo-toteutuksesta

Esimerkki MongoDB-dokumentista löytyy `data-template.json`:sta. Tämän mallin toteutumista
ei kuitenkaan valvota koodissa, joten ole skarppina datan tallennusoperaatioissa

### Markun pystytys

* Nimeä `settings-template.json` -> `settings.json` ja päivitä asetukset
* Asenna MongoDB ja varmista, että se pyörähtää koneella. Markku ei ole vastuussa Mongon käynnistämisestä, vaan tietokannan tulee olla käynnissä Markun käynnistyessä.
* Asenna python-rippuvuudet `requirements.txt`:n avulla