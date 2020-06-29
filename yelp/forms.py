from flask_wtf import FlaskForm
#will be writing python classes that will be representative of our forms
#will be automatically coverted into html forms within our template
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

#input form
class userInputForm(FlaskForm): #inherits from FlaskForm
	day = StringField('day', validators=[DataRequired()])#validators will be important classes
	time = StringField('time', validators=[DataRequired()])
	category = StringField('category', validators=[DataRequired()])
	location=StringField('location', validators=[DataRequired()])
	submit = SubmitField('Search')

