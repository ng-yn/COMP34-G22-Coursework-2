from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    '''
    Class for the profile form
    '''
    username = StringField(label='Username', validators=[DataRequired(message='Username is required')])
    bio = StringField(label='Bio', description='Write something about yourself')
    picture = FileField(label='Picture', validators=[FileAllowed(['jpeg', 'jpg', 'png'])])


