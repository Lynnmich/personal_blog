
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, widgets, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField


# Create a posts form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    slug = StringField("Slugfield", validators=[DataRequired()])
    latitude = StringField("Latitude", validators=[DataRequired()])
    longitude = StringField("Longitude", validators=[DataRequired()])
    # image1 = FileField("Image", validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    # image2 = FileField("Image", validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField("Submit")


#Create a destinations form
class DestinationForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    # content = StringField("Content", validators=[DataRequired()], widget=widgets.TextArea())
    submit = SubmitField("Submit")

# Create a form for admin
class AdminForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    admin_name = StringField("Admin_name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match!')])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create Login Form
class LoginForm(FlaskForm):
	admin_name = StringField("Admin_name", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Submit")
     

# Create a search form
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Search")