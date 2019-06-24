# MarkkuBot

MarkkuBot tai kutsumanimeltään Markku on TT-Kameroiden telegram-chattia varten tehty botti jonka päätehtävä on kertoa onko kerhohuoneella valot päällä. Markulle on ajan mittaan opetettu muitakin temppuja kuten kiittämisen jalo taito.

## Docker

Markun toteutus on siirretty Dockerissa pyöriväksi. Vaikka Markkua pystyy edelleen ajamaan ilman Dockerin apua, se helpottaa huomattavasti toimintaa. Kehittämiseen ja julkaisuun tarvitaan siis Dockeria ja Docker-composea.

### Kehitys

Kehitys onnistuu helpoiten samalla tavalla kuin tuotannossa eli *build_and_update.sh* tiedostolla joka tekee docker networking tjsp.

### Tuotanto

*Tähän saadaan toivottavasti automatisointi jatkossa.*

Markun image rakennetaan komennolla `docker build -t markkubot:latest .`.

Tuotantokoneella Markkua ajetaan docker-composella komennolla `docker-compose up -d`.

Ylläolevat komennot ovat kirjoitettu valmiiksi *build_and_update.sh* tiedostossa.

### .env

Kopsaa `.env.sample` ja nimeä uudelleen `.env`:iksi. Kirjoittele sinne fiksuja arvoja.

`POSTGRES_DB` on Postgresiin luotavan tietokannan nimi.

## Huomattavaa

Muista uuden botin privacy mode pois.

HUOM: Samasta koodiversiosta myös tägi githubiin samalla versionumerolla, `git tag -a x.x.x -m "x.x.x" && git push --tags`, `-a` tekee annotoidun tagin (joka on ihan hyvä olla) ja tällöin sille joutuu heittämään jonkun viestin.

## ROADMAP

* Githubista automatisoidut Docker-buildit: https://docs.docker.com/docker-hub/github/#github-organizations
* Tuotantoon joku haistelija, joka hakee uusimman buildin Docker Hubista ja käynnistää Markun uudelleen

