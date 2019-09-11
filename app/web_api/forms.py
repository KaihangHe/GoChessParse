from flask_wtf import FlaskForm
from wtforms import DateField,FileField,SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired,FileAllowed

class ImageForm(FlaskForm):
    image=FileField('',validators=[FileRequired(),FileAllowed(['jpg','png','jpeg'])])
    submit=SubmitField('Submit')