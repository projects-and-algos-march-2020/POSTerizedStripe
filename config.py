from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import stripe
import os

app = Flask(__name__)

# Stripe API
stripe_keys = {
    "secret_key":  os.environ['STRIPE_SECRET_KEY'],
    "publishable_key": os.environ['STRIPE_PUBLISHABLE_KEY']
}
stripe.api_key = stripe_keys['secret_key']

# for file uploading
app.config['UPLOAD_FOLDER'] = './static/images/uploads'

# configurations to tell our app about the database we'll be connecting to
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_dash.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "LOL"

bcrypt = Bcrypt(app)

# an instance of the ORM
db = SQLAlchemy(app)
# a tool for allowing migrations/creation of tables
migrate = Migrate(app, db)