from flask import redirect, request, Blueprint, make_response, jsonify
from firebase_admin import auth
from functools import wraps
import datetime

login_page = Blueprint('login_page', __name__,
                        template_folder='templates')

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

@login_page.route('/logout')
def logout():
    response = make_response(redirect('/'))
    response.set_cookie('session_cookie', '', expires=0)
    return response

@login_page.route('/trade_token_for_cookie', methods=['POST'])
def trade_token_for_cookie():
    id_token = request.form['idToken']
    expires_in = datetime.timedelta(days=5)

    session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
    response = jsonify({'status': 'success'})
    # Set cookie policy for session cookie.
    expires = datetime.datetime.now() + expires_in
    response.set_cookie('session_cookie', session_cookie, expires=expires, samesite='Lax', secure=True)

    return response
