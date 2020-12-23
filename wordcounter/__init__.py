import os
from flask import Flask
from . import counter 
from paths import paths

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)


    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    app.config['UPLOAD_FOLDER'] = paths['UPLOAD_FOLDER']

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(counter.bp)
    
    return app
