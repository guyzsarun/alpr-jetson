from flask import Response, Flask, request
from utils import line_notify

app = Flask(__name__)
@app.route("/" ,methods = ['POST'])
def streamFrames():
    file = request.files['media']
    file.save('tmp.jpg')
    line_notify('request','tmp.jpg',False)
    return 'OK'

if __name__ == '__main__':
    app.run("0.0.0.0", port="8000")