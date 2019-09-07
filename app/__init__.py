import os
from flask import Flask
from flask_bootstrap import Bootstrap


def create_app():
    '''

    :return:
    '''
    app = Flask(__name__)
    bootstrap = Bootstrap()
    bootstrap.init_app(app)
    app.config['SECRET_KEY']=os.environ.get('SECRET_KEY') or 'Hello,Nicapoet'
    from .web_api import upload_blueprint
    app.register_blueprint(upload_blueprint)
    return app
