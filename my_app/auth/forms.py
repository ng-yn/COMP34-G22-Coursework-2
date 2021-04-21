"""Classes for Signup and login forms"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, EqualTo, length, ValidationError

from my_app.models import User


class SignupForm(FlaskForm):
    # Fields for user input
    username = StringField(label='Username', validators=[InputRequired(message='A username is required')])
    email = EmailField(label='Email address', validators=[InputRequired(message='An email is required')])
    password = PasswordField(label='Password',
                             validators=[InputRequired(),
                                         length(min=4, max=16,
                                                message='Password must be between 4-16 characters long')])
    password_repeat = PasswordField(label='Repeat Password',
                                    validators=[InputRequired(), EqualTo('password', message='Passwords must match')])

    # Checks if email is already in the database
    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('An account is already registered for that email address')


class LoginForm(FlaskForm):
    # Fields for user input
    email = EmailField(label='Email address', validators=[InputRequired(message='An email is required')])
    password = PasswordField(label='Password',
                             validators=[InputRequired(),
                                         length(min=4, max=16,
                                                message='Passwords are 4-16 characters long')])
    remember = BooleanField('Remember me')

    # Checks if an existing account is already registered to this email, returns error if invalid
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('This email address is not registered')

    # Checks if the password is correct for existing account, returns error if invalid
    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user is not None:
            if User.check_password(user, password.data) is False:
                raise ValidationError('The password is incorrect')


class ForgotForm(FlaskForm):
    email = EmailField(label='Email address', validators=[InputRequired(message='An email is required')])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('This email address is not registered')


