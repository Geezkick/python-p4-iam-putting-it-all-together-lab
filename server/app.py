from flask import Flask, session
from flask_migrate import Migrate
from flask_restful import Api
from dotenv import load_dotenv
from server.config import db, bcrypt
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

    db.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    # Import models for Flask-Migrate
    from server.models import User, Recipe

    try:
        from server.resources import Signup, CheckSession, Login, Logout, RecipeIndex
        api.add_resource(Signup, '/signup')
        api.add_resource(CheckSession, '/check_session')
        api.add_resource(Login, '/login')
        api.add_resource(Logout, '/logout')
        api.add_resource(RecipeIndex, '/recipes')
    except ImportError as e:
        print(f"ImportError in app.py: {e}")
        raise

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)