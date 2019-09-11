from flask import render_template
from . import upload_blueprint
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
        image_file.save(os.path.abspath(os.path.dirname(__file__))+"/../../upload/1.jpg")
        print(image_file)
    #todo：调用cv_parse
    return render_template('upload.html',form=form)