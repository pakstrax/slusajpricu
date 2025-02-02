# Dokumentacija

## Opis
SlusajPricu je aplikacija za slusanje audio knjiga sa korisničkom autentifikacijom. Omogućava proveru članstva u biblioteci i autentifikaciju korisnika putem jedinstvenog koda i broja kartice i reprodukciju naslova kojima korisnik ima pristup.

## Struktura projekta
```
slusajpricu/
│── main.py 
│── biblioteka/
│   ├── utils/
│       ├── auth.py       # Autentifikacija korisnika
│       ├── constants.py  # Globalne konstante
│── knjige/
│   │── ... # knjige koje aplikacija trenutno moze da reprodukuje
│── static
│   │── css
│       │── home.css
│       │── login.css
│── templates
│   │── home.html
│   │── login.html
│── ...
```

## Instalacija i pokretanje

### 1Instalacija zavisnosti

Potrebno je da imate instaliran `Python 3.8+`. Zatim instalirajte potrebne pakete:
```bash
pip install requirements.txt
```

### Pokretanje aplikacije
```bash
python app.py
```
Aplikacija će se pokrenuti na `http://127.0.0.1:5000`

## Autentifikacija
Korisnici se autentifikuju pomoću jedinstvenog **library_code**, **broja kartice** i **imena**. Ako su podaci validni, korisnički podaci se čuvaju u sesiji.

## ️ Podešavanja
Svi ključni podaci i URL-ovi se nalaze u `./biblioteka/utils/constants.py`.