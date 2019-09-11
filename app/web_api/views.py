import os
import json
import time
from flask import render_template,jsonify
from werkzeug.utils import secure_filename

from .forms import ImageForm
from . import upload_blueprint
from ..cv_parse import output_result

UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + "/../../upload/"


@upload_blueprint.route('/', methods=['GET', 'POST'])
def upload():
    '''
    :return:
    '''
    form = ImageForm()
    if form.validate_on_submit():
        image_file = form.image.data
        filename = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '_' + image_file.name)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image_file.save(image_path)
        try:
            output = output_result(image_path, False)
        except ZeroDivisionError:
            return jsonify({'ret': -1, 'msg': 'detect fail'})
        else:
            print('POST output', output)
            return jsonify({'ret': 1, 'msg': 'detect succeed', 'output': output})
    return render_template('upload.html', form=form)
