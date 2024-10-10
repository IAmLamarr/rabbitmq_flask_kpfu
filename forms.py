from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Post title', validators=[DataRequired()])
    text = TextAreaField('Post text', validators=[DataRequired()])
    submit = SubmitField('Create')