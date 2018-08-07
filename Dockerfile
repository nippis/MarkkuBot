# Parent image
FROM python:3.7.0-slim

# Working directory
WORKDIR /src

# Kopioi tarvittavat tiedostot src:n alle
COPY markku.py /src
COPY requirements.txt /src
COPY masterlist.json /src

# Asenna riippuvuudet
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Aja markku, kun container käynnistetään
CMD ["python", "markku.py"]