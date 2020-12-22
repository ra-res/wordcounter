import os

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
            return render_template('index.html')
        else:
            flash('Incorrect file type, only PDF or TXT allowed')
            return redirect(request.url)    
    return render_template('index.html')