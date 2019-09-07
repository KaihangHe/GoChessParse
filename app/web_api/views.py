from flask import render_template
from . import upload_blueprint
from .forms import ImageForm

@upload_blueprint.route('/',methods=['GET','POST'])
def upload():
    '''

    :return:
    '''
    form=ImageForm()
    if form.validate_on_submit():
        image=form.image.data
        print(image)
    #todo：调用cv_parse
    return render_template('upload.html',form=form)