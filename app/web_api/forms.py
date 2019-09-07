from flask_wtf import FlaskForm
from wtforms import DateField,FileField,SubmitField
from wtforms.validators import DataRequired

class ImageForm(FlaskForm):
    image=FileField('',validators=[DataRequired()])
    submit=SubmitField('Submit')