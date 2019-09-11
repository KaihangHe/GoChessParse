from flask import render_template
from . import upload_blueprint
from ..cv_parse import output_result
from .forms import ImageForm
import os
@upload_blueprint.route('/',methods=['GET','POST'])
def upload():
    '''
    :return:
    '''
    form=ImageForm()
    if form.validate_on_submit():
        image_file=form.image.data
        print(image_file)
        image_path=os.path.abspath(os.path.dirname(__file__))+"/../../upload/1.jpg"
        image_file.save(image_path)
        output=output_result(image_path,False)
        print('POST output',output)
        return output
    return render_template('upload.html',form=form)