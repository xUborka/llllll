from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials
from cv import cv_page
from login import login_page, login_required
from translate.translate import translate_page


cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
app = Flask(__name__)
app.register_blueprint(cv_page)
app.register_blueprint(login_page)
app.register_blueprint(translate_page)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
@login_required
def main(user_data):
    context = {"user_id": user_data['user_id']}
    return render_template('main.html', context=context)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
