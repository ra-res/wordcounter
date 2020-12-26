import os, shutil
from flask import (
    Blueprint,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    session,
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from paths import paths

bp = Blueprint("/", __name__)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in paths["ALLOWED_EXTENSIONS"]
    )


def word_counter(filename):
    return len(open(os.path.join(current_app.config["UPLOADED_PATH"], filename), encoding="cp437").readlines()) or 0


def delete_files():
    app = current_app
    for filename in os.listdir(app.config["UPLOADED_PATH"]):
        file_path = os.path.join(app.config["UPLOADED_PATH"], filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


@bp.route("/", methods=["GET", "POST"])
def upload_file():
    app = current_app
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOADED_PATH"], filename))
            count = word_counter(filename)
            session['count'] = count
            delete_files()
        else:
            flash("Incorrect file type, only PDF or TXT allowed")
            return redirect(request.url)
    return render_template("index.html")
