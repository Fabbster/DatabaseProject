from flask import Flask
# from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
import os

MainPage = Flask(__name__)

@MainPage.route('/')
def index():
    title = 'Flask Website'
    app_name = 'My Flask App'
    return render_template('index.html', title=title, app_name=app_name)

app = Flask(__name__)
app.config.from_object(Config())
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost:3306/mydatabase'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.name

@app.route('/')
def index():
    user = User('John Doe', 'john@example.com')
    db.session.add(user)
    db.session.commit()
    return 'User added'

