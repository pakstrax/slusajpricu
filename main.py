from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_from_directory,
    abort,
)

from biblioteka.utils.constants import (
    LAT_TO_CLEAN_LAT,
    KNJIGE_PATH,
    URL
)

from srtools import cyrillic_to_latin
import requests
import json
import os
import re

app = Flask(__name__)
app.secret_key = 'key'


@app.route('/knjige/<path:filename>')
def serve_audio_files(filename):
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        return send_from_directory('knjige', filename)
    except FileNotFoundError:
        abort(404)


@app.route('/', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        # Ukoliko postoji otvorena sesija, redirectuj na biblioteka stranu
        return redirect(url_for('biblioteka'))

    url = URL
    r = requests.get(f"{url}/libraries")
    libraries = r.json() if r.status_code == 200 else []

    if request.method == 'POST':
        # Uzmi unete podatke i posalji request na mock endpoint
        code = request.form.get('library_code')
        ime = request.form.get('ime')
        broj_kartice = request.form.get('broj_kartice')

        if code and ime and broj_kartice:
            full = f"{url}/lending/{code}/{broj_kartice}/{ime}/"
            response = requests.get(full)

            if response.status_code == 200:
                # Spakuj relevantne informacije u sesiju
                session['user'] = {
                    'ime': ime,
                    'broj_kartice': broj_kartice,
                    'library_code': code
                }
                session['message'] = response.text
                # idi na biblioteka stranu
                return redirect(url_for('biblioteka'))

        # Renderuj login stranu
        return render_template(
            'login.html',
            error="Neuspešna prijava. Molimo Vas proverite unesene podatke.",
            libraries=libraries
        )

    return render_template('login.html', libraries=libraries)


@app.route('/biblioteka')
def biblioteka():
    # Ako ne postoji otvorena sesija, vrati se na login
    if 'user' not in session:
        return redirect(url_for('login'))

    # Procitaj prethodno spakovane pozajmljene knjige
    message = session.get('message', '')
    data = json.loads(message)

    books: list = []
    if 'lendings' in data:
        books = data['lendings']

    clean_books: list = []

    # ocisti imena knjiga i matchuj ih sa onima koje se nalaze u ./knjige
    for book in books:
        mp3_files = match_system(book)
        book['files'] = match_system(book)
        if mp3_files:
            clean_books.append(book)

    # Renderuj home stranu i na njoj pozajmljene knjige
    return render_template('home.html', books=clean_books)


def match_system(book: dict) -> list:
    listed: list = []

    # Ocisti imena knjiga i pretvori ih u celavu latinicu
    title = book['title']
    lat_title = cyrillic_to_latin(title).lower()
    lat_title_c = ""
    for character in lat_title:
        if character in LAT_TO_CLEAN_LAT:
            character = LAT_TO_CLEAN_LAT[character]
        lat_title_c += character
    clean_title = re.sub(r'[^a-z0-9]', "", lat_title_c)

    # Ako se cist naslov nalazi u putanji na kojoj su knjige,
    #  vrati folder sa istim imenom
    if clean_title in os.listdir(KNJIGE_PATH):
        path_to_check = os.path.join(KNJIGE_PATH, clean_title)
        listed = [
            os.path.join(KNJIGE_PATH, clean_title, file)
            for file in os.listdir(path_to_check) if file.endswith('.mp3')
        ]

    return sorted(listed)


if __name__ == '__main__':
    app.run(debug=True)
