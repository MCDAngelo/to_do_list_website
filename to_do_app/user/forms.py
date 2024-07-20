from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


password_validators = [DataRequired(), Length(min=8, max=20)]


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=password_validators)
    login_submit = SubmitField("Login")


class RegistrationForm(LoginForm):
    confirm_password = PasswordField("Confirm Password", validators=password_validators)
    register_submit = SubmitField("Register")
