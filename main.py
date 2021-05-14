from flask import Flask, render_template, redirect, request, jsonify, make_response
import firebase_admin
from firebase_admin import auth
import datetime
from functools import wraps
import os
import time

firebase_admin.initialize_app()
app = Flask(__name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_cookie = request.cookies.get('session_cookie')
        if not session_cookie:
            return redirect('/')
        try:
            decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
        except (auth.InvalidSessionCookieError, auth.UserNotFoundError) as e:
            print(e)
            return redirect('/')
        return f(decoded_claims, *args, **kwargs)
    return decorated_function

def format_server_time():
    serve_time = time.localtime()
    return time.strftime("%I:%M:%S %p", serve_time)

@app.route('/')
def index():
    context = { "server_time" : format_server_time()}
    return render_template('index.html', context=context)

@app.route('/logout')
@login_required
def logout(user_data):
    response = make_response(redirect('/'))
    response.set_cookie('session_cookie', '', expires=0)
    return response

@app.route('/create_anon_user', methods=['POST'])
def create_anon_user():
    id_token = request.form['idToken']
    expires_in = datetime.timedelta(days=5)

    session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
    response = jsonify({'status': 'success'})
    # Set cookie policy for session cookie.
    expires = datetime.datetime.now() + expires_in
    response.set_cookie('session_cookie', session_cookie, expires=expires, samesite='Lax', secure=True)

    return response

@app.route('/auth_needed')
@login_required
def auth_needed(user_data):
    uid = user_data['user_id']
    context = {"user_id": uid}
    return render_template('index.html', context=context)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)