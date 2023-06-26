import os
from os import environ, path
from flask import Flask, render_template, url_for
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from wtforms import TextAreaField


#Create a flask instance
app = Flask(__name__)
post = []

# General Configuration
basedir = os.path.abspath(os.path.dirname(__file__))

# Add my Database
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'posts.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret key
app.config['SECRET_KEY'] = "key"

# Initialize the dB
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Create a Blog post model
class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    subtitle = db.Column(db.String(200))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
    slug = db.Column(db.String(200))

    # Create a string
    #def __repr__(self):
        #return f'<Posts {self.title}>'

#Create a posts form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextAreaField())
    slug = StringField("Slugfield", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create route decorators
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/destinations')
def destinations():
    return render_template("destinations.html")

@app.route('/facts')
def facts():
    return render_template("facts.html")

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(title=form.title.data, subtitle=form.subtitle.data, content=form.content.data, slug=form.slug.data)
        # Clear the form after submission
        form.title.data = ''
        form.subtitle.data = ''
        form.content.data = ''
        form.slug.data =''

        # Add blogpost data to the database
        db.session.add(post)
        db.session.commit()

        # Return a message once submission is successful
        flash("Travel guide post submitted successfully!")

    # Redirect back to the webpage
    return render_template("add.html", form=form)

@app.route('/posts')
def posts():
    return render_template("posts.html")

# End of route decorators

# Custom Error page decorator
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# End of Custom Error page decorator

