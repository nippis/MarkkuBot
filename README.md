# MarkkuBot

MarkkuBot tai kutsumanimeltään Markku on TT-Kameroiden telegram-chattia varten tehty botti jonka päätehtävä on kertoa onko kerhohuoneella valot päällä. Markulle on ajan mittaan opetettu muitakin temppuja kuten kiittämisen jalo taito.

## Docker

Markun toteutus on siirretty Dockerissa pyöriväksi. Vaikka Markkua pystyy edelleen ajamaan ilman Dockerin apua, se helpottaa huomattavasti toimintaa. Kehittämiseen ja julkaisuun tarvitaan siis Dockeria ja Docker-composea.

### Kehitys

Posgresql lokaalisti tai konttiin pyörimään ja sinne tarvittavat taulut, käyttäjä ja oikeudet käyttäjälle.
Markkua voi tämän jälkeen ajaa joko lokaalisti `markku.py` tiedoston kautta tai kontissa.  

### Tuotanto

Markun image rakennetaan komennolla `docker build -t markkubot:latest .`.

Tietokantaimage ladataan tuotantokoneelle komennolla `docker pull postgresql`, minkä jälkeen kontin saa ajoon komennolla `sudo docker run --rm --name MarkkuDB --d -p 5432:5432 -v <polku lokaaliin volumeen>:/var/lib/postgresql/data postgres`.

Itse botin kontin saa ajoon komennolla `sudo docker run -d --network="host" --name MarkkuBot --restart on-failure markkubot`.

### .env

Kopsaa `.env.sample` ja nimeä uudelleen `.env`:iksi. Kirjoittele sinne fiksuja arvoja.

## Huomattavaa

Muista uuden botin privacy mode pois.

## ROADMAP

* Githubista automatisoidut Docker-buildit: https://docs.docker.com/docker-hub/github/#github-organizations

