from flask import Flask, render_template


#Create a flask instance and a route decorator
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/user/<name>')
def user():
    return "Hello "


# Custom Error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404