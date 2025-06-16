from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a secure key
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy()
migrate = Migrate()
api = Api()

db.init_app(app)
migrate.init_app(app, db)
api.init_app(app)