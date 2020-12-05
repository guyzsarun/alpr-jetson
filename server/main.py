import requests
from flask import Response, Flask, request

url = 'http://172.28.110.23:8000/open'

app = Flask(__name__)
@app.route("/open")
def open_gate():
    print('open gate')
    requests.post(url)
    return '200 OK'

if __name__ == '__main__':
    app.run("0.0.0.0", port="5000")