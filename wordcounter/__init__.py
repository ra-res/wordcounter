import os
from flask import Flask
from . import counter
from paths import paths
from flask_dropzone import Dropzone
from flask import request, render_template
from . import paths

basedir = os.path.abspath(os.path.dirname(__file__))

dropzone = Dropzone()


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        UPLOADED_PATH=os.path.join(basedir, "cvuploads"),
        DROPZONE_MAX_FILE_SIZE=10,
        DROPZONE_TIMEOUT=5 * 60 * 1000,
    )

    dropzone.init_app(app)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(counter.bp)

    return app
