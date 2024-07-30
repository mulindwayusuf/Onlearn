# from dataclasses import field
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, SelectField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from app.models import UserRole

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[(role.value, role.name.capitalize()) for role in UserRole], validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_role(self, field):
        if field.data not in UserRole.__members__:
            raise ValidationError('invalid role selected, please choose from parent, student or admin')
    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me',)
    submit = SubmitField('Login')

class SubjectForm(FlaskForm):
    subject_name = StringField('Subject Name', validators=[DataRequired()])
    description = TextAreaField('Subject Description', validators=[DataRequired()])
    submit = SubmitField('Create Subkect')
