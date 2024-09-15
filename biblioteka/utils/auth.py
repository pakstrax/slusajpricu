import requests
from flask import session, redirect, url_for

from biblioteka.utils.constants import URL

def list_libraries():

    response = requests.get(f"{URL}/libraries")
    libraries = response.json() if r.status_code == 200 else []
    return libraries


def authenticate(request):

    code = request.form.get('library_code')
    ime = request.form.get('ime')
    broj_kartice = request.form.get('broj_kartice')

    if code and ime and broj_kartice:
        full = f"{URL}/lending/{code}/{broj_kartice}/{ime}/"
        response = requests.get(full)

        if response.status_code == 200:
            session['user'] = {'ime': ime, 'broj_kartice': broj_kartice, 'library_code': code}
            session['message'] = response.text
            return redirect(url_for('biblioteka'))
    else:
        raise Exception("Neuspesna prijava.")

    return response
