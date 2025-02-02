# URL udaljenog API-ja koji se koristi za autentifikaciju i dohvatanje podataka
URL: str = "https://6e3d5b18-78dd-40d1-b201-53258ba38d60.mock.pstmn.io"

# Mapa karaktera za konverziju latiničnih slova u pojednostavljene verzije
LAT_TO_CLEAN_LAT: dict = {
    "ž": "z",
    "ć": "c",
    "č": "c",
    "š": "s",
    "đ": "dj"
}

# Putanja do direktorijuma u kojem se čuvaju podaci o knjigama
KNJIGE_PATH: str = 'knjige'