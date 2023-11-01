from flask import Flask, render_template, request, redirect, session
from flask_session import Session

from crypto_client import generate_keypair, plain_hot, encrypt_hot
from crypto_server import sum_encrypted
from db import create_table, get_qtd, get_all, new_result
from utils import show_title_private_key, show_private_key, show_encrypted_value, private_key_sessions

app = Flask(__name__)
app.secret_key = private_key_sessions()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

create_table()


############################ FLASK CONFIG ############################
@app.context_processor
def utility_processor():
    return dict(round=round,
                show_title_private_key=show_title_private_key,
                show_private_key=show_private_key,
                show_encrypted_value=show_encrypted_value)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('pages/404.jinja'), 404


############################ SERVER ############################
@app.route('/')
def index():
    if session.get('step') is None:
        session['step'] = 0
    return render_template('pages/index.jinja', qtd=get_qtd())


@app.route('/add', methods=['POST'])
def add():
    new_result(request.form['add-value'])
    return redirect('/')


@app.route('/retrieve', methods=['POST'])
def retrieve():
    encrypted_vector = session['crypto_hot_encoding']
    session['encrypted_sum'] = sum_encrypted(get_all(), encrypted_vector)
    session['step'] = 2

    return redirect('/')


############################ CLIENT ############################
@app.route('/generate', methods=['POST'])
def generate():
    session.clear()
    index = int(request.form['index'])
    scheme = request.form['scheme']
    qtd = get_qtd()

    # generate keys and encrypt the vector
    public, private = generate_keypair(scheme)
    hot_encoding = plain_hot(index, qtd)
    crypto_hot_encoding = encrypt_hot(hot_encoding, public)

    # put data in sessions
    session['scheme'] = scheme
    session['index_retrieve'] = index
    session['crypto_hot_encoding'] = crypto_hot_encoding
    session['hot_encoding'] = hot_encoding
    session['public'] = public
    session['private'] = private
    session['step'] = 1

    return redirect('/')


@app.route('/decrypt', methods=['POST'])
def decrypt():
    session['decrypted_sum'] = session['private'].decrypt(session['encrypted_sum'])
    session['step'] = 3

    return redirect('/')


@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    create_table()
    app.run(host="0.0.0.0")
