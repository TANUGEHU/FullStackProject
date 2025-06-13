from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, FileField
from flask_wtf.file import FileField, FileAllowed, FileRequired

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[validators.DataRequired("you need to enter a username")])
    password = PasswordField("Password", validators=[validators.DataRequired("you need to enter a password")])
    submit = SubmitField("Signup")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[validators.DataRequired("you need to enter a username")])
    password = PasswordField("Password", validators=[validators.DataRequired("you need to enter a password")])
    submit = SubmitField("Login")

class LogoutForm(FlaskForm):
    submit = SubmitField("Yes")

class UploadForm(FlaskForm):
    title = StringField("Title", validators=[validators.DataRequired("you need to enter a title")])
    description = StringField("Body", validators=[validators.DataRequired("you need to enter a body")])
    post = FileField("Media", validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'mp4', 'mov', 'avi'], 'Media files only!')
    ])
    submit = SubmitField("Upload")

class UpdateForm(FlaskForm):
    title = StringField("Title", validators=[validators.DataRequired("you need to enter a title")])
    description = StringField("Body", validators=[validators.DataRequired("you need to enter a body")])
    submit = SubmitField("Update")
