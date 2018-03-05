import os
from flask import Flask, render_template, request
from werkzeug import secure_filename

# running state code

UPLOAD_FOLDER = "/home/ankush/Desktop/uploadedfiles/"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello_world():
    return "Hello World"


@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    global s
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        s = filename
        file.save(filename)
        return "uploaded"


@app.route("/recognize", methods=['GET'])
def recognize_file():
    import classifier

    output = classifier.infer(s)
    return output


if __name__ == '__main__':
    app.run(host='0.0.0.0')
