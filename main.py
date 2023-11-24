import os
from flask import Flask, jsonify, send_from_directory, render_template, request, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
from werkzeug.utils import secure_filename
import uuid

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    storage_uri="memory://",
    default_limits=["10 per minute"],
    strategy="fixed-window",
)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def config_get():
    with open('data/settings.json') as f:
        data = json.load(f)
    return data

def jsonsend(result='default', message='Welcome to CDNServer'):
    js0n = {
        'errors': [
            {
                'code': 'default',
                'message': '{}'.format(message),
                'author': 'github.com/reques6e',
                'server': [
                    {'load': '{}'.format(result)}
                ]
            }
        ]
    }
    return js0n

def allowed_file(filename):
    return True

def generate_uuid_filename(filename):
    new_filename = str(uuid.uuid4()) + os.path.splitext(filename)[-1]
    return secure_filename(new_filename)

@app.route('/')
def main():
    return jsonify(jsonsend()), 200

@app.route('/upload')
def upload():
    return render_template('index.html')

    
@app.route('/cdn/<path:filename>', methods=['GET', 'POST'])
def cdn(filename):
    if request.method == 'POST' and filename == 'upload':
        if 'file' not in request.files:
            return jsonify(jsonsend(message='No file part')), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify(jsonsend(message='No selected file')), 400
        if file and allowed_file(file.filename):
            new_filename = generate_uuid_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(file_path)
            return redirect(url_for('cdn', filename=new_filename))
        else:
            return jsonify(jsonsend(message='File type not allowed')), 400
    elif filename == 'about':
        data = config_get()
        result = data.get('config_load_type', 'default_value')
        return jsonify(jsonsend(result)), 200
    else:
        file_path = os.path.join('uploads', filename)
        if os.path.isfile(file_path):
            return send_from_directory('uploads', filename)
        else:
            return jsonify(jsonsend(message='File not found!')), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)