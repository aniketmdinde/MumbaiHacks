from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

mongo = PyMongo()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'MumHacks'
    app.config['MONGO_URI'] = 'mongodb+srv://aniketmdinde100:Aniket*99@mumhacks.vl8mb.mongodb.net/MumHacks?retryWrites=true&w=majority&appName=MumHacks'

    mongo.init_app(app)
    bcrypt.init_app(app)

    from .views import views
    from .auth import auth
    from .database import database

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(database,url_prefix='/')

    return app