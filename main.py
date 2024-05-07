from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import time

import fun


app = Flask(__name__)

directory_name="path/downloads"
if not os.path.exists(directory_name):
     os.makedirs(directory_name) 


ALLOWED_EXTENSIONS = set(['pdf', 'txt'])
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), directory_name))
# app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1000 * 1000  # 500 MB
app.config['CORS_HEADER'] = 'application/json'

def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    current_time_stamp = time.time()
    result = {
        "message":"Hello World from python",
        "status":True,
        "time_stamp":current_time_stamp
    }
    return jsonify(result)

@app.route('/api/v1/sum',methods=['POST'])
def sum_function():
    sum = fun.sum(10,2)
    result = {
        "message":"Custom message will come here",
        "status":False,
        "sum":sum
    }
    return jsonify(result)

@app.route('/upload', methods=['POST', 'GET'])
def fileUpload():
    if request.method == 'POST':
        file = request.files.getlist('files')
        filename = ""
        print(request.files, "....")
        for f in file:
            print(f.filename)
            filename = secure_filename(f.filename)
            print(allowedFile(filename))
            if allowedFile(filename):
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                return jsonify({'message': 'File type not allowed'}), 400
        return jsonify({"name": filename, "status": "success"})
    else:
        return jsonify({"status": "Upload API GET Request Running"})

if __name__ == "__main__":
    app.run(debug = True)