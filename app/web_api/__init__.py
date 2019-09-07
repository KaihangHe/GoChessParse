from flask import Blueprint

upload_blueprint=Blueprint('upload',__name__)

from . import views,forms,errors