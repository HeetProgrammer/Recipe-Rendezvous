from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from directory.models import User

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_validate):
        duplicate = User.query.filter_by(username=username_to_validate.data).first()
        print(duplicate)
        if duplicate:
            raise ValidationError("Username Exists. Please try a different one")
    
    def validate_email_address(self, email_to_validate):
        duplicate = User.query.filter_by(email_address=email_to_validate.data).first()
        if duplicate:
            raise ValidationError("Email Address Exists. Please try a different one")

        
    username = StringField(label='Username', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=8), DataRequired()] )
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')



class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')