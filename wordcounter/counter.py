import os, shutil
from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from paths import paths

bp = Blueprint('/', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in paths['ALLOWED_EXTENSIONS']

def word_counter(filename):
    file = open(os.path.join(paths['UPLOAD_FOLDER'], filename), encoding="cp437")
    size = len(file.readlines())
    return size

def delete_files():
    for filename in os.listdir(paths['UPLOAD_FOLDER']):
        file_path = os.path.join(paths['UPLOAD_FOLDER'], filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

@bp.route('/', methods=['GET', 'POST'])
def upload_file():
    app = current_app
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(f"{word_counter(filename)}words")
            delete_files()
            return render_template('index.html')
        else:
            flash('Incorrect file type, only PDF or TXT allowed')
            return redirect(request.url)    
    return render_template('index.html')