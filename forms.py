# import required flask forms libraries
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import Form, SelectField, SubmitField, TextAreaField, TextField, validators, ValidationError
from wtforms.validators import DataRequired, Length
import sqlite3

# create class for add form 
class add(FlaskForm):
    item = StringField("item add",[validators.length(min=1, max=40), validators.input_required()])
