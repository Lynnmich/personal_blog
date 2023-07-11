import os
from os import environ, path
from flask import Flask, render_template, url_for, flash, redirect, session, request
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, widgets, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import werkzeug 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_ckeditor import CKEditor
from flask_ckeditor import CKEditorField
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_googlemaps import GoogleMaps, Map
from werkzeug.utils import secure_filename


#Create a flask instance
app = Flask(__name__)
post = []
ckeditor = CKEditor(app)

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

# Flask login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_admin(admin_id):
    return Admin.query.get(int(admin_id))

# Google Maps API Key
app.config["GOOGLEMAPS_KEY"] = "AIzaSyDKeFfXleXLNlQD_nISlxMN-ZBo2ThX7AU"
GoogleMaps(app)

# Get the absolute path of the project directory
# UPLOAD_FOLDER = 'static/images/'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Create a Blog post model
class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.Date, default=date.today)
    content = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    # image1 = db.Column(db.String, nullable=False)
    # image2 = db.Column(db.String, nullable=False)

    # Create a string
    #def __repr__(self):
        #return f'<Posts {self.title}>'

# Create a posts form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    # content = StringField("Content", validators=[DataRequired()], widget=widgets.TextArea())
    content = CKEditorField('Content', validators=[DataRequired()])
    slug = StringField("Slugfield", validators=[DataRequired()])
    latitude = StringField("Latitude", validators=[DataRequired()])
    longitude = StringField("Longitude", validators=[DataRequired()])
    # image1 = FileField("Image", validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    # image2 = FileField("Image", validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField("Submit")



# Create a Destinations model
class Destinations(db.Model):
    __tablename__ = 'destinations'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.Date, default=date.today)
    content = db.Column(db.Text, nullable=False)


    # Create a string
    #def __repr__(self):
        #return f'<Destinations {self.title}>'

#Create a destinations form
class DestinationForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    # content = StringField("Content", validators=[DataRequired()], widget=widgets.TextArea())
    submit = SubmitField("Submit")


# Create an Admin Model
class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    admin_name = db.Column(db.String(20), nullable=False, unique=True)
    date_added = db.Column(db.Date, default=date.today)
    email = db.Column(db.String(128), nullable=False, unique=True )
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not readable')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
        # Create a string
    #def __repr__(self):
        #return f'<Admin {self.name}>'



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
        '''
        # Save the uploaded images
        image1 = form.image1.data
        image2 = form.image2.data

        filename1 = secure_filename(image1.filename)
        filename2 = secure_filename(image2.filename)

        image1_path = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        image2_path = os.path.join(app.config['UPLOAD_FOLDER'], filename2)

        image1.save(image1_path)
        image2.save(image2_path) '''

        post = Posts(
            title=form.title.data, 
            subtitle=form.subtitle.data, 
            content=form.content.data, 
            slug=form.slug.data, 
            latitude=form.latitude.data, 
            longitude=form.longitude.data
            #image1=image1_path,
            #image2=image2_path
        )
        

        # Clear the form after submission
        form.title.data = ''
        form.subtitle.data = ''
        form.content.data = ''
        form.slug.data =''
        form.latitude.data = ''
        form.longitude.data = ''

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
    post = Posts. query.get_or_404(id)
    mymap = Map(
        identifier="post_map",
        lat=post.latitude,
        lng=post.longitude,
        markers=[(post.latitude, post.longitude)])
    return render_template('post.html', post=post, mymap=mymap)

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.slug = form.slug.data
        post.content = form.content.data
        post.latitude = form.latitude.data
        post.longitude = form.longitude.data


        # Commit changes to the database
        db.session.add(post)
        db.session.commit()

        flash(" Travel Guide has been updated successfully!")
        return redirect(url_for("post", id=post.id))
    
    form.title.data = post.title
    form.subtitle.data = post.subtitle
    form.slug.data = post.slug
    form.content.data = post.content
    form.latitude.data = post.latitude
    form.longitude.data = post.longitude
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

# Create an Admin page
@app.route('/admin')
def admin():
    # Retrieve all admins from the database
    admin = Admin.query.order_by(Admin.id)
    return render_template("admin.html", admin=admin)

@app.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    name = None
    form = AdminForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin is None:
            hashed_password = generate_password_hash(form.password_hash.data, 'sha256')
            admin = Admin(name=form.name.data, admin_name=form.admin_name.data, email=form.email.data, password_hash=hashed_password)
            db.session.add(admin)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.admin_name.data = ''
        form.email.data = ''
        form.password_hash.data =''

        flash("Admin added successfully!")
        my_admin = Admin.query.order_by(Admin.id)
        return render_template("add_admin.html",
        form=form,
        name=name,
        my_admin=my_admin)
    
    return render_template("add_admin.html", form=form, name=name)

@app.route('/admin/delete/<int:id>')
def delete_admin(id):
    admin_delete = Admin.query.get_or_404(id)

    try:
        db.session.delete(admin_delete)
        db.session.commit()

        flash("Admin deleted!")

        # Return all admins from the db
        admin = Admin.query.order_by(Admin.date_added)
        return render_template("admin.html", admin=admin)

    except:
        # Error message
        flash("There was a problem deleting the admin")

        # Return all admins from the db
        admin = Admin.query.order_by(Admin.date_added)
        return render_template("admin.html", admin=admin)

# Update Database 
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    name_to_update = Admin.query.get_or_404(id)
    form = AdminForm(obj=name_to_update)
    if form.validate_on_submit():
        name_to_update.name = form.name.data
        name_to_update.email = form.email.data
        name_to_update.password = form.password_hash.data

        try:
            db.session.commit()
            flash('Admin credentials updated successfully!')
            return redirect(url_for('admin'))
        except:
            flash('Oops! There was an error updating Admin credentials')

    return render_template("update.html", form=form, name_to_update=name_to_update)


@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        post.searched = form.searched.data
        posts = posts.filter(Posts.title.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()
        return render_template("search.html", 
                               form=form,
                               searched = post.searched,
                               posts = posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(admin_name=form.admin_name.data).first()
        if admin:
            if check_password_hash(admin.password_hash, form.password.data):
                login_user (admin)
                flash("Logged in Successfully!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong password. Please try again")
        else:
            flash("Admin doesn't exist")

    return render_template('login.html', form=form)



'''@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')'''

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # Retrieve all travel guides and destinations from the database
    guides = Posts.query.order_by(Posts.date_posted).all()
    destinations = Destinations.query.order_by(Destinations.date_posted).all()
    return render_template('dashboard.html', guides=guides, destinations=destinations)



@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully")
    return redirect(url_for('login'))


''' @app.route('/add', methods=['POST'])
def upload():
    uploaded_file = request.files['image']
    if uploaded_file:
        # Save the file to the upload folder
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='images/' + filename), code=301)'''
 

# End of Route Decorators

# Pass information to the navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


# Custom Error page decorator
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# End of Custom Error page decorator

