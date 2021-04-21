from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError
from my_app.models import Profile



class ProfileForm(FlaskForm):
    '''Class for the profile form'''
    username = StringField(label='Username', validators=[DataRequired(message='Username is required')])
    bio = StringField(label='Bio', description='Write something about yourself')
    picture = FileField(label='Picture', validators=[FileAllowed(['jpeg', 'jpg', 'png'])])

    # def validate_username(self, username):
    #     profile = Profile.query.filter_by(username=username.data).first()
    #     if profile is not None:
    #         raise ValidationError('Username already exists, please choose another username')
