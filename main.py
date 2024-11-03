from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, abort
from biblioteka.utils.constants import LAT_TO_CLEAN_LAT, KNJIGE_PATH
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
        return redirect(url_for('biblioteka'))

    url = f"https://6e3d5b18-78dd-40d1-b201-53258ba38d60.mock.pstmn.io"
    r = requests.get(f"{url}/libraries")
    libraries = r.json() if r.status_code == 200 else []

    if request.method == 'POST':
        code = request.form.get('library_code')
        ime = request.form.get('ime')
        broj_kartice = request.form.get('broj_kartice')

        if code and ime and broj_kartice:
            full = f"{url}/lending/{code}/{broj_kartice}/{ime}/"
            response = requests.get(full)

            if response.status_code == 200:
                session['user'] = {'ime': ime, 'broj_kartice': broj_kartice, 'library_code': code}
                session['message'] = response.text
                return redirect(url_for('biblioteka'))

        return render_template(
            'login.html',
            error="Neuspešna prijava. Molimo Vas proverite unesene podatke.",
            libraries=libraries
        )

    return render_template('login.html', libraries=libraries)


@app.route('/biblioteka')
def biblioteka():
    if 'user' not in session:
        return redirect(url_for('login'))

    message = session.get('message', '')
    data = json.loads(message)

    books = []
    if 'lendings' in data:
        books = data['lendings']

    clean_books = []

    for book in books:
        mp3_files = match_system(book)
        book['files'] = match_system(book)
        if mp3_files:
            clean_books.append(book)

    return render_template('home.html', books=clean_books)


def match_system(book: dict):
    listed = []
    title = book['title']
    lat_title = cyrillic_to_latin(title).lower()
    lat_title_c = ""
    for character in lat_title:
        if character in LAT_TO_CLEAN_LAT:
            character = LAT_TO_CLEAN_LAT[character]
        lat_title_c += character
    clean_title = re.sub(r'[^a-z0-9]', "", lat_title_c)

    if clean_title in os.listdir(KNJIGE_PATH):
        path_to_check = os.path.join(KNJIGE_PATH, clean_title)
        listed = [
            os.path.join(KNJIGE_PATH, clean_title, file)
            for file in os.listdir(path_to_check) if file.endswith('.mp3')
        ]

    return sorted(listed)


if __name__ == '__main__':
    app.run(debug=True)
