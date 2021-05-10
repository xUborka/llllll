from flask import Flask, render_template
import os
import time

app = Flask(__name__)

def format_server_time():
    serve_time = time.localtime()
    return time.strftime("%I:%M:%S %p", serve_time)

@app.route('/')
def index():
    context = { "server_time" : format_server_time() }
    return render_template('index.html', context=context)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))