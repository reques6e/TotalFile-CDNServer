import os
import json
import uuid

from flask import Flask, render_template, request, send_from_directory, abort

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

with open('data/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
    config_server = config['server']

app.config['UPLOAD_FOLDER'] = config_server['path_files']

def allowed_file_size(file_size, max_size):
    return file_size <= max_size * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config_server['allowed_files']

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html'), 405

@app.route('/')
def index():
    return render_template('index.html', mail=config_server['mail'])

@app.route('/upload', methods=['POST'])
def upload():
    if request.remote_addr not in config_server['allowed_ips'] and '*' not in config_server['allowed_ips']:
        return 'Доступ запрещен', 403
    
    if 'file' not in request.files:
        return 'Файл не выбран', 400
    
    file = request.files['file']

    if file.filename == '':
        return 'Не выбран не один файл', 400
    
    if not allowed_file(file.filename):
        return f'Неверный формат файла, разрешённые форматы: {config_server["allowed_files"]}', 400
    
    if not allowed_file_size(request.content_length, config_server['limit']):
        return f'На сервере установлен лимит ({config_server["limit"]}MB)', 400

    filename = str(uuid.uuid4())
    file_extension = file.filename.rsplit('.', 1)[1].lower()
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename + '.' + file_extension))
    file_url = f"{config_server['protocol']}://{config_server['domain']}/files/{filename}.{file_extension}"

    return f'{file_url}', 200

@app.route('/files/<path:filename>')
def uploaded_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        abort(404)

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host=config_server['domain'], port=config_server['port'], debug=True)