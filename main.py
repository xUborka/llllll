from flask import Flask, render_template, request
import firebase_admin
from flask.json import jsonify
from cv import cv_page
from login import login_page, login_required
import requests
import os


firebase_admin.initialize_app()
app = Flask(__name__)
app.register_blueprint(cv_page)
app.register_blueprint(login_page)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=["POST"])
@login_required
def submit(user_data):
    uid = user_data['user_id']
    code = request.form['code']
    # response = requests.post("http://localhost:8080/python/execute", json={'uid': uid, 'code': code})
    response = requests.post(os.environ.get("CODE_RUNNER") + "/python/execute", json={'uid': uid, 'code': code})
    return response.text

@app.route('/main')
@login_required
def main(user_data):
    uid = user_data['user_id']
    context = {"user_id": uid}
    return render_template('main.html', context=context)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)