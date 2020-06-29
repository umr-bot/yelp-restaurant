from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class LocationForm(FlaskForm): #a flaskform class for the location textbox for the user input, used primarily to use validators
    location = StringField('Location',  validators=[DataRequired()])
    submit = SubmitField('Submit')
