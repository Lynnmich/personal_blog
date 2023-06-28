import os
from os import environ, path
from flask import Flask, render_template, url_for, flash, redirect
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, widgets
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
#from wtforms import TextArea


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
    content = StringField("Content", validators=[DataRequired()], widget=widgets.TextArea())
    slug = StringField("Slugfield", validators=[DataRequired()])
    submit = SubmitField("Submit")


#Create a Destinations model
class Destinations(db.Model):
    __tablename__ = 'destinations'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

    # Create a string
    #def __repr__(self):
        #return f'<Posts {self.title}>'

#Create a destinations form
class DestinationForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=widgets.TextArea())
    submit = SubmitField("Submit")


# Create route decorators
@app.route('/')
def index():
    return render_template("index.html")

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
    # Retrieve all posts from the database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)

@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.slug = form.slug.data
        post.content = form.content.data

        # Commit changes to the database
        db.session.add(post)
        db.session.commit()

        flash(" Travel Guide has been updated successfully!")
        return redirect(url_for("post", id=post.id))
    form.title.data = post.title
    form.subtitle.data = post.subtitle
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html', form=form)

@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post_delete = Posts.query.get_or_404(id)

    try:
        db.session.delete(post_delete)
        db.session.commit()

        flash("Travel guide deleted!")

        # Return all posts from the db
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)

    except:
        # Error message
        flash("There was a problem deleting the guide")

        # Return all posts from the db
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)

# End of route decorators

# Route decorators for destinations page
@app.route('/add_destination', methods=['GET', 'POST'])
def add_destination():
    form = DestinationForm()

    if form.validate_on_submit():
        destination = Destinations(title=form.title.data, content=form.content.data)
        
        # Clear the form after submission
        form.title.data = ''
        form.content.data = ''

        # Add destination data to the database
        db.session.add(destination)
        db.session.commit()

        # Return a message once submission is successful
        flash("Destination information submitted successfully!")

    # Redirect back to the webpage
    return render_template("add_destination.html", form=form)

@app.route('/destinations') 
def destinations():
    # Retrieve all destinations from the database
    destinations = Destinations.query.order_by(Destinations.date_posted)
    return render_template("destinations.html", destinations=destinations)

@app.route('/destinations/<int:id>')
def destination(id):
    destination = Destinations.query.get_or_404(id)
    return render_template('destination.html', destination=destination)

@app.route('/destinations/edit/<int:id>', methods=['GET', 'POST'])
def edit_destination(id):
    destination = Destinations.query.get_or_404(id)
    form = DestinationForm()
    if form.validate_on_submit():
        destination.title = form.title.data
        destination.content = form.content.data

        # Commit changes to the database
        db.session.add(destination)
        db.session.commit()

        flash("Destination has been updated successfully!")
        return redirect(url_for("destination", id=destination.id))
    form.title.data = destination.title
    form.content.data = destination.content
    return render_template('edit_destination.html', form=form)

@app.route('/destinations/delete/<int:id>')
def delete_destination(id):
    dest_delete = Destinations.query.get_or_404(id)

    try:
        db.session.delete(dest_delete)
        db.session.commit()

        flash("Destination deleted!")

        # Return all destinations from the db
        destinations = Destinations.query.order_by(Destinations.date_posted)
        return render_template("destinations.html", destinations=destinations)

    except:
        # Error message
        flash("There was a problem deleting the destination")

        # Return all posts from the db
        destinations = Destinations.query.order_by(Destinations.date_posted)
        return render_template("destinations.html", destinations=destinations)


# Custom Error page decorator
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# End of Custom Error page decorator

