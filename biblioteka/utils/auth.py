import requests
from flask import session, redirect, url_for, Request

from biblioteka.utils.constants import URL


# Ovo se trenutno ne koristi, autentikacija je implementirana u main.py


def list_libraries() -> list:
    """
    Dohvata listu biblioteka sa udaljenog API-ja.

    Returns:
        list: Lista biblioteka ako je zahtev uspešan, inače prazna lista.
    """
    response = requests.get(f"{URL}/libraries")
    libraries = response.json() if response.status_code == 200 else []
    return libraries


def authenticate(request: Request) -> requests.Response:
    """
    Autentifikuje korisnika na osnovu podataka iz forme.

    :param request: HTTP zahtev koji sadrži podatke za autentifikaciju.
    :return: Redirektuje korisnika na stranicu biblioteke ako je prijava
    uspešna, inače vraća HTTP odgovor sa greškom.

    :raises: Exception: Ako korisnik nije uneo sve potrebne podatke ili
    autentifikacija nije uspešna.
    """

    code = request.form.get('library_code')
    ime = request.form.get('ime')
    broj_kartice = request.form.get('broj_kartice')

    if code and ime and broj_kartice:
        full = f"{URL}/lending/{code}/{broj_kartice}/{ime}/"
        response = requests.get(full)

        if response.status_code == 200:
            session['user'] = {
                'ime': ime,
                'broj_kartice': broj_kartice,
                'library_code': code
            }
            session['message'] = response.text
            return redirect(url_for('biblioteka'))
    else:
        raise Exception("Neuspesna prijava.")

    return response
