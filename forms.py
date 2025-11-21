from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class ConsultationForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    subject = StringField('Subject', validators=[Length(max=50)])
    situation = TextAreaField('Describe the Situation', validators=[Length(max=500)])
    assessment = TextAreaField('Personal Assessment', validators=[Length(max=500)])
    language = SelectField('Language', choices=[('English', 'English'), ('Spanish', 'Spanish')], default='English')
    submit = SubmitField('Consult the Oracle')

class NoteForm(FlaskForm):
    notes = TextAreaField('Your Notes')
    submit = SubmitField('Save Notes')
