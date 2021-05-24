import os
from flask import Flask, request
import subprocess

app = Flask(__name__)


@app.route("/")
def hello_world():
    return ''

@app.route("/python/execute", methods=["POST"])
def python_execute():
    payload = request.get_json()
    print(payload)
    with open("dummy_output.py", "w") as out_file:
        out_file.write(payload['code'])
    sp = subprocess.run(["python", "dummy_output.py"], capture_output=True)
    return {'stdout': sp.stdout}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))